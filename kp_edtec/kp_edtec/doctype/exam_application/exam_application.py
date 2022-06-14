# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from kp_edtec.kp_edtec.doctype.semesters.semesters import get_courses
from frappe.utils import today,getdate


class ExamApplication(Document):
    def validate(self):
        self.validate_courses()
        check_duplicate_application(self)
        self.validate_exam_declaration()
    
    def validate_courses(self):
        for course in self.exam_application_courses :
            if course.course:
                if course.course not in [ c.course for c in frappe.db.get_all('Course Enrollment', {'student':self.student, 'academic_year':self.program_academic_year, 'academic_term':self.academic_term, 'status':['!=', "Completed"]}, 'course') ]:
                    frappe.throw("Course <b>{0}</b> not enrolled by student <b>{1}</b>".format(course.course, self.student))

    def validate_exam_declaration(self):
        block_list=get_blocklist_declarations(self.student)
        
        if self.exam_declaration in block_list:
            frappe.throw("Student Exists in Block List")

        # if len(frappe.get_all("Program Enrollment",{"student":self.student,"docstatus":1},['programs',"program"]))!=0:
        #     for d in frappe.get_all("Program Enrollment",{"student":self.student,"docstatus":1},['programs',"program"]):
        #         filters={
        #             "disabled":0,
        #             "is_application_required":1,
        #             "application_form_start_date":["<=",today()],
        #             "application_form_end_date":[">=",today()],}
        #         for ex in frappe.get_all("Exam Declaration",filters,["name","exam_name"],as_list=1):
        #             if ex[0] in block_list:
        #                 frappe.throw("Student Exists in Block List")

@frappe.whitelist()
def make_fees(source_name, target_doc=None):
    from kp_edtec.kp_edtec.doctype.program_enrollment import get_program_enrollment
    def set_missing_values(source, target):
        target.student_email=frappe.db.get_value("Student",target.student,"student_email_id")
        if get_program_enrollment(source.student):
            target.program_enrollment=get_program_enrollment(source.student)['name']

        if target.program_enrollment:
            target.student_category=frappe.db.get_value("Program Enrollment",target.program_enrollment,"student_category")
            target.student_batch=frappe.db.get_value("Program Enrollment",target.program_enrollment,"student_batch_name")
            
        fee_structure=get_fee_structure("Exam Declaration",source.exam_declaration,frappe.db.get_value("Student",target.student,"student_category"))
        if fee_structure:
            target.fee_structure=fee_structure.get('fee_structure')
            target.due_date=fee_structure.get('due_date')
            for fc in frappe.get_all("Fee Component",{"parent":target.fee_structure},['fees_category','amount','description']):
                target.append("components",{
                    "fees_category":fc.fees_category,
                    "amount":fc.amount,
                    "description":fc.description
                })

    doclist = get_mapped_doc("Exam Application", source_name,   {
        "Exam Application": {
            "doctype": "Fees",
            "field_map": {
                "current_program":"programs",
                "current_semester":"program",
                "program_academic_year":"academic_year"
            },
            "validation": {
                "docstatus": ["=", 1]
            }
        },
    }, target_doc, set_missing_values)

    return doclist
    
def get_fee_structure(doctype,docname,category):
    if len(frappe.get_all("Exam Declaration Fee Item",{"parenttype": doctype, "parent":docname ,"student_category":category},["fee_structure","amount"]))>0:
        return frappe.get_all("Exam Declaration Fee Item",{"parenttype": doctype, "parent":docname ,"student_category":category},["fee_structure","amount","due_date"])[0]
    return ""


@frappe.whitelist()
def get_declaration_details(declaration,student):
    category=frappe.db.get_value("Student",student,"student_category")
    doc=frappe.get_doc("Exam Declaration",declaration)
    return {"exam_fees":get_fees_amount(doc,category),"semesters":doc.semesters}


def get_fees_amount(doc,category):
    fees=0
    if doc.exam_fees_applicable=="YES":
        for d in doc.get("fee_structure"):
            if d.student_category==category:
                fees=d.amount
    return fees

@frappe.whitelist()
def get_declaration(doctype, txt, searchfield, start, page_len, filters):
    lst = []
    dct= {}
    for i in frappe.get_all("Exam Declaration",{"exam_program":filters.get("program"),"docstatus":1},['name','exam_name']):
            if i.name not in lst and i.exam_name not in lst:
                lst.append(i.name)
                lst.append(i.exam_name)
                dct.update({i.name:i.exam_name})
    return [(d,y) for d,y in dct.items()]

@frappe.whitelist()
def get_exam_declaration(doctype, txt, searchfield, start, page_len, filters):
    student=filters.get("student")
    filters.pop("student")
    block_list=get_blocklist_declarations(student)
    if len(frappe.get_all("Program Enrollment",{"student":student,"docstatus":1},['programs',"program"]))!=0:
        for d in frappe.get_all("Program Enrollment",{"student":student,"docstatus":1},['programs',"program"]):
            filters.update({"exam_program":d.get("programs"),"docstatus":1})
            filters.update({"name":['like', '%{}%'.format(txt)]})
            declarations=[]
            for ex in frappe.get_all("Exam Declaration",filters,["name","exam_name"],as_list=1):
                if ex[0] not in block_list:
                    declarations.append(ex)
            return declarations
    else:
        return []

def check_duplicate_application(doc):
    for d in frappe.get_all("Exam Application",{"student":doc.student,"exam_declaration":doc.exam_declaration,"academic_term":doc.academic_term,"docstatus":1}):
        if d.name!=doc.name:
            frappe.throw("Application Already Exists <b>{0}</b>".format(d.name))

@frappe.whitelist()
def get_courses_from_declaration(exam_declaration,student):
    declaration=frappe.get_doc("Exam Declaration",exam_declaration)
    result = []
    for course in [d.courses for d in declaration.courses_offered]:
        for enrollemt in frappe.get_all("Course Enrollment",{"student":student,"course":course,"status":("!=","Completed")}):
            semester = frappe.db.get_value('Program Course', {'course': course,"parent":["IN",[d.semester for d in declaration.semesters]]}, 'parent')
            for cr in frappe.db.get_all('Course', {'name':course}, ['name','course_code','course_name']):
                cr.update({"semester":semester})
                result.append(cr)
    return result

def get_blocklist_declarations(student):
    declarations=[]
    for d in frappe.get_all("Student Block Item",{"student":student,"docstatus":1},['parent'],group_by="parent"):
        for bl in frappe.get_all("Student Exam Block List",{"name":d.parent},['exam_declaration']):
            declarations.append(bl.exam_declaration)
    return declarations