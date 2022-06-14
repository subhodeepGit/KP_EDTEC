# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from kp_edtec.kp_edtec.utils import academic_term

class AssessmentCreditsAllocation(Document):
    def validate(self):
        self.validate_student()
        self.validate_assessment_criteria()
        self.validate_marks()
        self.validate_duplicate_record()
        academic_term(self)
    
    def validate_duplicate_record(self):
        if self.student and self.course and self.assessment_criteria and self.academic_year and self.academic_term:
            for a in frappe.get_all('Assessment Credits Allocation', {'student':self.student, 'course':self.course,'assessment_criteria':self.assessment_criteria,'academic_year':self.academic_year, 'academic_term':self.academic_term, 'docstatus':('!=', 2)}):
                if a.name and a.name != self.name:
                    frappe.throw("The data is already exist in <b>{0}</b>".format(a.name))
    
    def validate_student(self):
        for st in frappe.get_all("Student",{"name":self.student},["enabled"]):
            if not st.enabled:
                frappe.throw("Student is not <b>Enabled</b>")

    def validate_assessment_criteria(self):
        lst = []
        for i in frappe.get_all("Course Enrollment",{'student':self.get("student"),"course":self.get("course"),"status":("!=","Completed")},['name']):
            fltr={"parent":i.get("name")}
            for j in frappe.get_all("Credit distribution List",fltr,["assessment_criteria"]):
                lst.append(j.assessment_criteria)

        if self.assessment_criteria not in lst:
            frappe.throw("Please Select the Assessment Criteria In Course <b>{0}</b>".format(self.get("course")))

    def validate_marks(self):
        for cr in self.get("final_credit_item"):
            addition=(flt(cr.earned_marks)+flt(cr.grace_marks))
            if addition>flt(cr.total_marks):
                frappe.throw("Grace Marks Cannot be Greater than <b>{0}</b>".format(flt(cr.total_marks)-flt(cr.earned_marks)))
       
        if self.grace_marks > flt(self.out_of_marks):
            frappe.throw("Grace Marks <b>{0}</b> Cannot be Greater than out of marks <b>{1}</b>".format(self.grace_marks, self.out_of_marks))
        
        if flt(self.final_marks)>flt(self.out_of_marks):
            frappe.throw("<b>Final Marks</b> Cannot be Greater Than <b>Out of Marks</b>")

        if flt(self.earned_credits)>flt(self.total_credits):
            frappe.throw("<b>Earned Credits</b> Cannot be Greater Than <b>Total Credits</b>")

    @frappe.whitelist()
    def get_course_details(self):
        course=frappe.get_doc("Course",self.course)
        for d in course.get("credit_distribution"):
            if self.assessment_criteria == d.assessment_criteria:
                return d

@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                        Select 
                                enroll_cr.course,
                                enroll_cr.course_name,
                                enroll_cr.course_code
                        from `tabProgram Enrollment` enroll
                        left join `tabProgram Enrollment Course` enroll_cr on enroll.name=enroll_cr.parent 
                        where enroll.student='{0}' and enroll.docstatus=1  and (enroll_cr.course LIKE %(txt)s or enroll_cr.course_name LIKE %(txt)s or enroll_cr.course_code LIKE %(txt)s) 
                        GROUP BY enroll_cr.course
                    """.format(filters.get("student")),dict(txt="%{}%".format(txt)))    

@frappe.whitelist()
def get_assessment_criteria(doctype, txt, searchfield, start, page_len, filters):
    lst = []
    for i in frappe.get_all("Course Enrollment",{'student':filters.get("student"),"course":filters.get("course"),"status":("!=","Completed")},['name']):
        fltr={"parent":i.get("name")}
        if txt:
            fltr.update({'assessment_criteria': ['like', '%{}%'.format(txt)]})
        for j in frappe.get_all("Credit distribution List",fltr,["assessment_criteria"]):
            lst.append(j.assessment_criteria)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_course_assessment(student,course,assessment_criteria):
    total_earned_marks=total_total_marks=weightage_marks=0
    data_list=[]
    len_ca = len(frappe.get_all("Course Assessment",{"student":student,"course":course,"assessment_criteria":assessment_criteria, "docstatus":1},["name","earned_marks","total_marks"]))
    if len_ca > 0 :
        for d in frappe.get_all("Course Assessment",{"student":student,"course":course,"assessment_criteria":assessment_criteria, "docstatus":1},["name","earned_marks","total_marks"]):
            total_earned_marks+=flt(d.earned_marks)
            total_total_marks+=flt(d.total_marks)
            for cr in frappe.get_all("Credit distribution List",{"parent":course,"assessment_criteria":assessment_criteria},['total_marks']):
                weightage_marks=flt((total_earned_marks/total_total_marks)*flt(cr.total_marks))
            d.update({"total_earned_marks":total_earned_marks,"total_total_marks":total_total_marks,"weightage_marks":weightage_marks})
            data_list.append(d)
        return data_list
    else:
        return data_list
        frappe.msgprint("No evaluation found for student.")

