# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class CourseAssessment(Document):
    def validate(self):
        self.validate_marks()

    def validate_marks(self):
        if flt(self.earned_marks)>flt(self.total_marks):
            frappe.throw("<b>Earned Marks</b> Cannot be Greater Than <b>Total Marks</b>")

@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    data=frappe.db.sql("""select 
                                ce.course,ce.course_name,ce.course_code
                        from 
                            `tabCourse Enrollment` ce 
                        where status!="Completed" and student='{0}' and ce.academic_year='{1}' and ce.academic_term='{2}' and (ce.course like '%{3}%' or ce.course_name like '%{3}%' or ce.course_code like '%{3}%') """
                        .format(filters.get("student"),filters.get("academic_year"),filters.get("academic_term"),txt))
    return data if data else []
    
@frappe.whitelist()
def get_assessment_criteria(doctype, txt, searchfield, start, page_len, filters):
    lst = []
    for i in frappe.get_all("Course Enrollment",{'student':filters.get("student"),"course":filters.get("course"),"status":("!=","Completed")},['name']):
        fltr={"parent":i.get("name")}
        if txt:
            fltr.update({"assessment_criteria":txt})
        for j in frappe.get_all("Credit distribution List",fltr,["assessment_criteria"]):
            if j.assessment_criteria not in lst:
                if j.assessment_criteria:
                    lst.append(j.assessment_criteria)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_details(student,course):
    for ce in frappe.get_all("Course Enrollment",{"student":student,"course":course},["program_enrollment"]):
        return frappe.db.get_value("Program Enrollment",ce.program_enrollment,["programs","program","academic_year","academic_term"],as_dict=1)

@frappe.whitelist()
def get_exam_declaration(doctype, txt, searchfield, start, page_len, filters):
    student=filters.get("student")
    filters.pop("student")
    declarations=[]
    if len(frappe.get_all("Program Enrollment",{"student":student, "docstatus":1},['programs',"program"]))!=0:
        for d in frappe.get_all("Program Enrollment",{"student":student, "docstatus":1},['programs',"program","name"]):
            filters.update({"exam_program":d.get("programs"),"docstatus":1})
            for ed in frappe.get_all("Exam Declaration",filters,["name","exam_name"],as_list=1):
                # if frappe.db.get_value("Examination Semester",{"parent":ed[0],"semester":d.get("program")}):
                declarations.append(ed)
            return declarations
    else:
        return []

@frappe.whitelist()
def get_assessment_criteria_detail(course,criteria):
    for data in frappe.get_all("Credit distribution List",{"parent":course,"assessment_criteria":criteria},["credits","total_marks"]):
        return data

@frappe.whitelist()
def get_exam_assessment_plan(doctype, txt, searchfield, start, page_len, filters):
    plan=[]

    for pl in frappe.get_all("Exam Assessment Plan",{"name": ["like", "%{0}%".format(txt)],"programs":filters.get("programs"),"program":filters.get("program"),"academic_year":filters.get("academic_year"),"exam_declaration":filters.get("exam_declaration"),"docstatus":filters.get("docstatus")},as_list=1):
        for cr in frappe.get("Course Assessment Plan Item",{"parent":pl.name,"course":filters.get("course")}):
            plan.append(pl)

    return plan