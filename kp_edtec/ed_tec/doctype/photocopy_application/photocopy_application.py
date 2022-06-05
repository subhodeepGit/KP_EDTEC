# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import getdate
from kp_edtec.ed_tec.utils import get_courses_by_semester

class PhotocopyApplication(Document):
    def validate(self):
        if self.docstatus==1:
            self.status="Submitted"
            has_photocopy=False
            for d in self.photocopy_item:
                if d.photocopy:
                    has_photocopy=True
            if has_photocopy:
                self.status="Phocopy Uploaded"
        elif self.docstatus==2:
            self.status="Cancelled"
        else:
            self.status="Draft"
        date_validation(self)
    # pass
    # def validate(doc):
    #   lst = []
    #   admint_card_number = frappe.db.get_value("Student Admit Card",{"student_roll_no":doc.get("student")},['name'])
    #   for i in doc.get("photocopy_item",{"parent":doc.get('name')},['course']):
    #       lst.append(i.get("course"))
    #   for j in frappe.get_all("Admit Card Course",{"parent":admint_card_number,'parenttype':"Student Admit Card"},['courses']):
    #       if j.get('courses') not in lst:
    #           doc.append("photocopy_item", {
    #               "course" :j.get('courses')
    #               })
    #   for k in frappe.get_all("Admit Card Course",{"parent":admint_card_number,'parenttype':"Exam Declaration"},['courses']):
    #       if k.get('courses') not in lst:
    #           doc.append("photocopy_item", {
    #               "course" :k.get('courses')
    #               })
    
#fees from Photocopy
@frappe.whitelist()
def make_fees(source_name, target_doc=None):
    def set_missing_value(source, target):
        for fe_structure in frappe.get_all("Exam Declaration Fee Item",{"parent":source.get("post_exam_declaration")},['fee_structure','due_date']):
            for ex in frappe.get_all("Exam Declaration",{"name":source.get("exam_declaration")},["academic_year"]):
                for d in frappe.get_all("Program Enrollment",{"student":source.student,"docstatus":1,"academic_year":ex.academic_year},["name","programs","program","student_category","academic_year","academic_term","student_batch_name"]):
                    target.program_enrollment=d.name
                    target.programs = d.get("programs")
                    target.program = d.get("program")
                    target.student_category=d.get("student_category")
                    target.academic_year=d.get("academic_year")
                    target.academic_term=d.get("academic_term")
                    target.student_batch=d.get("student_batch_name")
            target.student_email=frappe.db.get_value("Student",{"name":source.student},["user"])
            target.fee_structure   = fe_structure.fee_structure
            target.due_date=fe_structure.due_date
            for fc in frappe.get_all("Fee Component",{"parent":target.fee_structure},['fees_category','amount','description']):
                target.append("components",{
                    "fees_category":fc.fees_category,
                    "amount":fc.amount,
                    "description":fc.description
                })

    doclist = get_mapped_doc("Photocopy Application", source_name, {
    "Photocopy Application": {
        "doctype": "Fees"
    }
    }, target_doc,set_missing_value)

    return doclist

#Reevaluation Application
@frappe.whitelist()
def make_reevaluation_application(source_name, target_doc=None):
    def set_missing_value(source, target):
        pass
    doclist = get_mapped_doc("Photocopy Application", source_name, {
    "Photocopy Application": {
        "doctype": "Reevaluation Application"
    }
    }, target_doc,set_missing_value)

    return doclist
@frappe.whitelist()
def get_amount(post_exam):
    return frappe.db.get_value("Exam Declaration Fee Item",{"parent":post_exam,"parenttype":"Post Exam Declaration"},['amount'])

@frappe.whitelist()
def get_exam_declaration(doctype, txt, searchfield, start, page_len, filters):
    if len(frappe.get_all("Program Enrollment",{"student":filters.get("student"), "docstatus":1},['programs',"program"]))!=0:
        for d in frappe.get_all("Program Enrollment",{"student":filters.get("student"), "docstatus":1},['programs',"program"]):
            return frappe.get_all("Exam Declaration",{"docstatus":1,"exam_program":d.get("programs"),"name":['like', '%{}%'.format(txt)]},["name","exam_name"],as_list=1)
    else:
        return []
@frappe.whitelist()
def get_post_exam_declaration(doctype, txt, searchfield, start, page_len, filters):
    for d in frappe.get_all("Program Enrollment",{"student":filters.get("student"), "docstatus":1},['programs',"program"]):
        exam_list=[]
        for ex in frappe.get_all("Exam Declaration",{"docstatus":1,"exam_program":d.get("programs"),}):
            exam_list.append(ex.name)
        return frappe.get_all("Post Exam Declaration",{"exam_declaration":["IN",exam_list],"name":['like', '%{}%'.format(txt)]},["name"],as_list=1)


@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    if filters.get("exam_declaration"):
        for d in frappe.get_all("Exam Declaration",{"name":filters.get("exam_declaration"),"docstatus":1},["name"]):
            courses = get_courses_by_semester([sem.semester for sem in frappe.get_all("Examination Semester",{"parent":d.name},["semester"] )])
            if courses:
                return frappe.db.sql("""select name,course_name,course_code from tabCourse
                    where name in ({0}) and (name LIKE %s or course_name LIKE %s or course_code LIKE %s)
                    limit %s, %s""".format(", ".join(['%s']*len(courses))),
                    tuple(courses + ["%%%s%%" % txt, "%%%s%%" % txt,"%%%s%%" % txt, start, page_len]))
            return []

def date_validation(doc):
    post_exam_declaration=frappe.get_doc("Post Exam Declaration",doc.post_exam_declaration)
    if not (getdate(post_exam_declaration.start_date)<=getdate(doc.application_date) and getdate(post_exam_declaration.end_date)>=getdate(doc.application_date)):
        frappe.throw("<b>Application Date</b> Should be In Between Post Exam Declaration<b>Start Date And End Date</b>")
