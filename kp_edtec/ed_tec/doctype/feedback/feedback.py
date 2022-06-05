# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Feedback(Document):
	pass

# @frappe.whitelist()
# def get_student_program(doctype, txt, searchfield, start, page_len, filters):
# 	fltr = {}
# 	if txt:
# 		fltr.update({"programs":txt})

# 	fltr.update({"student":filters.get("student")})
# 	data = frappe.get_all("Program Enrollment",fltr,['programs'],as_list=1)
# 	return data

@frappe.whitelist()
def get_student_program(doctype, txt, searchfield, start, page_len, filters):
   return frappe.db.sql("""SELECT distinct(ced.programs) as student, st.title as student_name 
   from `tabCurrent Educational Details` ced left join `tabStudent` st on st.name=ced.parent 
   where enabled=1 and st.name='{0}'""".format(filters.get("student")))    


@frappe.whitelist()
def get_faculty(doctype, txt, searchfield, start, page_len, filters):
	fltr = {}
	if txt:
		fltr.update({"parent":txt})

	fltr.update({"student_group":filters.get("student_group")})

	data = frappe.get_all("Instructor Log",fltr,['parent'],as_list=1)
	return data