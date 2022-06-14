# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import getdate

class ReevaluationApplication(Document):
	def validate(self):
		date_validation(self)

@frappe.whitelist()
def make_fees(source_name, target_doc=None):
	def set_missing_value(source, target):
		for fe_structure in frappe.get_all("Exam Declaration Fee Item",{"parent":source.get("post_exam_declaration")},['fee_structure','due_date']):
			for ex in frappe.get_all("Exam Declaration",{"name":source.get("exam_declaration"),"docstatus":1},["academic_year"]):
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

	doclist = get_mapped_doc("Reevaluation Application", source_name, {
	"Reevaluation Application": {
		"doctype": "Fees"
	}
	}, target_doc,set_missing_value)

	return doclist

def date_validation(doc):
	post_exam_declaration=frappe.get_doc("Post Exam Declaration",doc.post_exam_declaration)
	if not (getdate(post_exam_declaration.start_date)<=getdate(doc.application_date) and getdate(post_exam_declaration.end_date)>=getdate(doc.application_date)):
		frappe.throw("<b>Application Date</b> Should be In Between Post Exam Declaration<b>Start Date And End Date</b>")