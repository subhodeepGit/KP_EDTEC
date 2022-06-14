# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from kp_edtec.kp_edtec.doctype.branch_sliding_application.branch_sliding_application import date_validation
import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission


class ExamPaperSetting(Document):
    def validate(self):
        date_validation(self)
       
    def after_save(self):
        self.set_user_permission()
        
    def set_user_permission(self):
        if self.examiner:
            self.set_instructor_permission(self.examiner)
        if self.moderator_name:
            self.set_instructor_permission(self.moderator_name)

    def on_trash(self): 
        self.delete_permission()

    def delete_permission(self):
        for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
            frappe.delete_doc("User Permission",d.name)

    def set_instructor_permission(self, instructor):
        for i in frappe.get_all("Instructor",{"name":instructor},['employee']):
            if i.get('employee'):
                for emp in frappe.get_all("Employee", {'name':i.get('employee')}, ['user_id']):
                    if emp.get('user_id'):
                        add_user_permission("Exam Paper Setting",self.name, emp.get('user_id'), self)
            else:
                frappe.msgprint("Instructor {0} is not employee".format(instructor))

# bench execute kp_edtec.kp_edtec.doctype.exam_paper_setting.exam_paper_setting.make_exam_paper_setting_from_sssessment_plan
def make_exam_paper_setting_from_sssessment_plan():
    for ap in frappe.get_all("Exam Assessment Plan",{'docstatus':1,"paper_setting_start_date":getdate(today())}):
        ap=frappe.get_doc("Exam Assessment Plan",ap.name)
        for ex in ap.get("examiners_list"):
            doc=frappe.new_doc("Exam Paper Setting")
            doc.examiner=ex.paper_setter
            doc.posting_date=today()
            doc.program=ap.program
            doc.course=ap.course
            doc.assessment_plan=ap.name
            doc.academic_year=ap.academic_year
            doc.from_time=ap.from_time
            doc.to_time=ap.to_time
            doc.academic_term=ap.academic_term
            doc.schedule_date=ap.schedule_date
            for cr in ap.get('assessment_criteria'):
                doc.append("assessment_plan_criteria",{
                    'assessment_criteria':cr.assessment_criteria,
                    'maximum_score':cr.maximum_score
                })
            doc.save()
            if get_userid(doc.examiner):
                share_document(doc)
                assigned_to(doc,ap.paper_setting_end_date)

def share_document(doc):
    doc_share=frappe.new_doc("DocShare")
    doc_share.user= get_userid(doc.examiner).user_id
    doc_share.share_doctype="Exam Paper Setting"
    doc_share.share_name=doc.name
    doc_share.read=1
    doc_share.write=1
    doc_share.insert(ignore_permissions=True)

def assigned_to(doc,due_date):
    todo = frappe.new_doc("ToDo")
    todo.owner = get_userid(doc.examiner).user_id
    todo.description = "Paper Setting Document Shared With Examiner <b>{0}</b> ".format(doc.examiner)
    todo.date = due_date
    todo.reference_type = "Exam Paper Setting"
    todo.reference_name = doc.name
    todo.insert(ignore_permissions=True)

def get_userid(examiner):
    data=frappe.db.sql("""Select em.user_id from `tabEmployee` em
                        Left Join `tabInstructor` ins on em.name=ins.employee
                    Where ins.name='{0}'""".format(examiner),as_dict=1)
    if len(data)>0:
        return data[0]

# bench execute kp_edtec.kp_edtec.doctype.exam_paper_setting.exam_paper_setting.delete_share_document
def delete_share_document():
    for ap in frappe.get_all("Exam Assessment Plan",{'docstatus':1,"paper_setting_end_date":getdate(today())}):
        for eps in frappe.get_all("Exam Paper Setting",{"assessment_plan":ap.name}):
            for ds in frappe.get_all("DocShare",{"share_doctype":"Exam Paper Setting","share_name":eps.name}):
                frappe.delete_doc("DocShare",ds.name)

# @frappe.whitelist()
# def get_examiner_details(examiner):
#     doc=frappe.get_doc("Instructor",examiner)
#     print("///////doc.get('instructor_log')", doc.get('instructor_log'))
#     if doc.get('instructor_log'):
#         return doc.get('instructor_log')
#     else:
#         frappe.msgprint("Instructor log ")

def date_validation(doc):
    validation=True
    if doc.schedule_date:
        for d in frappe.get_all("Exam Assessment Plan",{"program":doc.program,"paper_setting_start_date":("<=",doc.schedule_date),"paper_setting_end_date":(">=",doc.schedule_date)}):
            validation=False
        if validation:
            frappe.throw("Exam Assessment Plan paper setting dates Not Exists")
        
@frappe.whitelist()
def filter_examiner(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Paper Setter Item",{'parent':filters.get('assessment_plan'),'course':filters.get('course'),'paper_setter': ['like', '%{}%'.format(txt)]},['paper_setter','full_name'],as_list=1)

@frappe.whitelist()
def filter_moderator(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("moderator List",{'parent':filters.get('assessment_plan'),'course':filters.get('course'),'moderator': ['like', '%{}%'.format(txt)]},['moderator','moderator_name'],as_list=1)

@frappe.whitelist()
def filter_course(doctype, txt, searchfield, start, page_len, filters):
    course_list = frappe.get_all("Course Assessment Plan Item",{'parent':filters.get('assessment_plan'),'course': ['like', '%{}%'.format(txt)]},pluck='course')
    return frappe.get_all("Course",{"name":["IN",course_list]},['name','course_name','course_code'],as_list=1)

@frappe.whitelist()
def get_assessment_plan_details(assessment_plan):
    return frappe.get_all("Exam Assessment Plan",{'name':assessment_plan},['programs', 'program', 'academic_year', 'academic_term'])

@frappe.whitelist()
def get_examiner_moderator(assessment_plan,course):
    examiner=""
    for i in frappe.get_all("Paper Setter Item",{'parent':assessment_plan,'course': course},['paper_setter']):
        examiner=i.paper_setter
    
    moderator=""
    for i in frappe.get_all("moderator List",{'parent':assessment_plan,'course': course},['moderator']):
        moderator=i.moderator
   
    return {'examiner':examiner, 'moderator':moderator}