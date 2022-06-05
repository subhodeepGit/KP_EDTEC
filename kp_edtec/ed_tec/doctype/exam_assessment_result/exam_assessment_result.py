# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import flt
from erpnext.education.api import get_grade
from erpnext.education.api import get_assessment_details
from frappe.utils.csvutils import getlink
import erpnext.education
from kp_edtec.ed_tec.utils import duplicate_row_validation

class ExamAssessmentResult(Document):
    def validate(self):
        duplicate_row_validation(self, "assessment_result_item", ['course','assessment_criteria'])
        self.set_evaluation_result_item()
        self.set_grade()
        if len(self.assessment_result_item) > 0:
            self.calculate_sgpa()
        self.validate_duplicate()
    
    @frappe.whitelist()
    def set_assessment_result_item(self):
        self.assessment_result_item = []
        result = []
        for allocation in frappe.get_all("Assessment Credits Allocation",{"docstatus":1,"student":self.student,"academic_year":self.academic_year,"academic_term":self.academic_term},["course","earned_credits","total_credits","final_marks","out_of_marks","assessment_criteria"]):
            row = {
                "course":allocation.course,
                "earned_cr":allocation.earned_credits,
                "total_cr":allocation.total_credits,
                "earned_marks":allocation.final_marks,
                "total_marks":allocation.out_of_marks,
                "assessment_criteria":allocation.assessment_criteria
            }
            if row not in result:
                result.append(row)
        for r in result:
            self.append("assessment_result_item", r)
                
    def on_submit(self):
        self.complete_course_enrollment()
        # self.update_program_enrollment_result()

    def set_grade(self):
        self.total_score = 0.0
        self.maximum_score=0.0
        total_pass=0
        for d in self.assessment_result_item:
            if flt(d.total_marks) > 0.0 :
                d.grade = get_grade(self.grading_scale, (flt(d.earned_marks)/flt(d.total_marks))*100)
                self.total_score += flt(d.earned_marks)
                self.maximum_score +=flt(d.total_marks)
                
            for g in frappe.get_all("Grading Scale Interval",{"parent":self.grading_scale,"grade_code":d.grade},['result']):
                if g.result=="PASS":
                    d.result="P"
                else:
                    d.result="F"
                    
            for cr in frappe.get_all("Credit distribution List",{"parent":d.course,"assessment_criteria":d.assessment_criteria},['passing_marks']):
                if flt(cr.passing_marks) > flt(d.earned_marks):
                    d.result="F"
                else:
                    d.result="P"

            if d.result=="P":
                total_pass+=1

        if len(self.assessment_result_item)==total_pass and total_pass > 0:
            self.result="Pass"  
        
        elif total_pass!=0:
            self.result="Backlog"

        if self.maximum_score > 0:
            self.grade = get_grade(self.grading_scale, (self.total_score/self.maximum_score)*100)

        for d in self.evaluation_result_item:
            if flt(d.total_marks) > 0.0 :
                d.grade = get_grade(self.grading_scale, (flt(d.earned_marks)/flt(d.total_marks))*100)
                self.total_score += flt(d.earned_marks)
                self.maximum_score +=flt(d.total_marks)
            assessment_criteria = [a.assessment_criteria for a in self.assessment_result_item if a.course == d.course ]
            for cr in frappe.get_all("Credit distribution List",{"parent":d.course,"assessment_criteria":assessment_criteria[0]},['passing_marks']):
                if flt(cr.passing_marks) > flt(d.earned_marks):
                    d.result="F"
                else:
                    d.result="P"
                
            for g in frappe.get_all("Grading Scale Interval",{"parent":self.grading_scale,"grade_code":d.grade},['result']):
                if g.result=="PASS":
                    d.result="P"
                else:
                    d.result="F"

    def validate_duplicate(self):
        assessment_result = frappe.get_list("Exam Assessment Result", filters={"name": ("not in", [self.name]),
            "student":self.student, "docstatus":1, 'programs':self.programs, 'program':self.program})
        if assessment_result:
            frappe.throw(_("Exam Assessment Result record {0} already exists.").format(getlink("Exam Assessment Result",assessment_result[0].name)))

    def calculate_sgpa(self):
        earn_and_garde=earn=0
        # evaluation_result_item
        for d in self.get("assessment_result_item"):
            if self.grade and self.grading_scale:
                if d.earned_cr:
                    earn+=d.earned_cr
                    for g in frappe.get_all("Grading Scale Interval",{"parent":self.grading_scale,"grade_code":d.grade},['grade_point']):
                        earn_and_garde+=((d.earned_cr or 0)*(g.grade_point or 0))
        if earn > 0 :
            self.sgpa=(earn_and_garde/earn)

    def complete_course_enrollment(self):
        for item in self.get("evaluation_result_item"):
            if item.result=="P":
                for enroll in frappe.get_all("Course Enrollment",{"student":self.student,"course":item.course}):
                    course_enroll=frappe.get_doc("Course Enrollment",enroll.name)
                    course_enroll.status="Completed"
                    course_enroll.save()

    def set_evaluation_result_item(self):
        duplicate=[]
        self.set("evaluation_result_item",[])
        for row in self.get("assessment_result_item"):
            earned_cr=total_cr=earned_marks=total_marks=0
            if row.course not in duplicate:
                for d in self.get("assessment_result_item"):
                    duplicate.append(row.course)
                    if row.course==d.course:
                        earned_cr+=flt(d.earned_cr)
                        total_cr+=flt(d.total_cr)
                        earned_marks+=flt(d.earned_marks)
                        total_marks+=flt(d.total_marks)
                self.append("evaluation_result_item",{
                    "course":row.course,
                    "course_name":frappe.db.get_value("Course",row.course,'course_name'),
                    "course_code":frappe.db.get_value("Course",row.course,'course_code'),
                    "earned_cr":earned_cr,
                    "total_cr":total_cr,
                    "earned_marks":earned_marks,
                    "total_marks":total_marks
                })
 
@frappe.whitelist()
def get_grade_result(grading_scale, earned_marks, total_marks):
    grade = get_grade(grading_scale, (flt(earned_marks)/flt(total_marks))*100)
    for g in frappe.get_all("Grading Scale Interval",{"parent":grading_scale,"grade_code":grade},['result']):
        if g.result=="PASS":
            result="P"
        else:
            result="F"
        return {'grade': grade, 'result':result}        

@frappe.whitelist()
def get_assessment_status(student,semester,academic_year,academic_term):
    completed=False
    for course_enroll in frappe.get_all("Course Enrollment",{"student":student,"academic_year":academic_year,"academic_term":academic_term, "semester": semester}):
        for enroll_item in frappe.get_all("Credit distribution List",{"parent":course_enroll.name},['assessment_criteria']):
            completed=True
            if len(frappe.get_all("Assessment Credits Allocation",{'student':student,'assessment_criteria':enroll_item.assessment_criteria,"academic_year":academic_year,"academic_term":academic_term,"docstatus":1}))==0:
                completed=False 
    return completed  

@frappe.whitelist()
def get_student_details(student):
    if student:
        data=frappe.get_all("Program Enrollment",{'student':student,'docstatus':1},['programs', 'program', 'academic_year', 'academic_term'],limit=1)
        if len(data)>0:
            return data[0]  
        else:
            frappe.throw("Program not enrolled by student {0}".format(student))  
        
@frappe.whitelist()
def filter_courses(doctype, txt, searchfield, start, page_len, filters):
    if len(frappe.get_all("Exam Application",{'student':filters.get('student'),'docstatus':1},['name'])) > 0:
        for app in frappe.get_all("Exam Application",{'student':filters.get('student'),'docstatus':1},['name']):
            return frappe.get_all("Exam Application Courses",{'parent':app.get('name'),'course_name': ['like', '%{}%'.format(txt)]},['course', 'course_name'], as_list=1)
    else:
        frappe.msgprint("Exam Application not found for student")
        return []
