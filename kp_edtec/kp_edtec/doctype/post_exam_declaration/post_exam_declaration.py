# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate
# from kp_edtec.kp_edtec.notification.custom_notification import post_exam_declaration_save

class PostExamDeclaration(Document):
    def validate(self):
        date_validation(self)
        # if self.is_new():
        #     post_exam_declaration_save(self)

@frappe.whitelist()
def get_fee_structure(doctype, txt, searchfield, start, page_len, filters):
    lst = []
    for i in frappe.get_all("Exam Declaration",{"name":filters.get("declaration")},['exam_program']):
        lst.append(i.get("exam_program"))
    
    
    return frappe.get_all("Fee Structure",{"programs":["in",lst],"fee_type":"Post Exam Fees"},['name','programs'],as_list = 1)

def date_validation(doc):
    exam_declaration=frappe.get_doc("Exam Declaration",doc.exam_declaration)
    if getdate(exam_declaration.exam_end_date)>=getdate(doc.start_date):
        frappe.throw("<b>Start Date</b> Should be Greater Than Exam Declaration <b>Exam End Date</b>")