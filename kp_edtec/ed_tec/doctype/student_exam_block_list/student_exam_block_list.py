# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from kp_edtec.ed_tec.notification.custom_notification import student_exam_block_submit
from frappe.utils import today, getdate

class StudentExamBlockList(Document):
    def on_submit(self):
        if self.send_notification:
            student_exam_block_submit(self)
        
@frappe.whitelist()
def get_declar(doctype, txt, searchfield, start, page_len, filters):
    lst = []
    dct = {}
    for i in frappe.get_all("Exam Declaration",{"exam_program":filters.get("program_of_exam"),"disabled":0, "docstatus":1, 'block_list_display_date':('>=', getdate(today()))},['name','exam_name']):
        if i.name not in lst and i.exam_name not in lst:
            lst.append(i.name)
            lst.append(i.exam_name)
            dct.update({i.name:i.exam_name})
    return [(d,y) for d,y in dct.items()]

@frappe.whitelist()
def get_student(student, target_doc = None):
        fname = frappe.db.get_value("Student",{"name":student},['first_name'])
        if frappe.db.get_value("Student",{"name":student},['last_name']):
            return fname +" "+frappe.db.get_value("Student",{"name":student},['last_name']) 
        else:
            return fname
            
@frappe.whitelist()
def get_student_by_program(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""Select distinct(st.name),st.title from `tabStudent` st left join `tabCurrent Educational Details` ced on ced.parent=st.name where ced.programs='{0}' and (st.name like '%{1}%' or st.title like '%{1}%')""".format(filters.get("program"),txt))