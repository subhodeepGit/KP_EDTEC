# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from kp_edtec.kp_edtec.doctype.fees import on_submit
import frappe
from frappe.desk.desk_page import get
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import today,getdate

class StudentExchangeApplicant(Document):
	def validate(self):
		if self.get("__islocal"):
			if self.student_category and self.academic_year and self.student_exchange_program:
				for d in get_document_list_by_category(self.student_category , self.academic_year, self.student_exchange_program):
					if d.document_name not in [dl.document_name for dl in self.get("document_list")]:
						self.append("document_list",{
							"document_name":d.document_name,
							"mandatory":d.mandatory
						})
		mobile_number_validation(self)
		date_validation(self)
	
	def on_change(self):
		if self.docstatus==1:
			validate_attachment(self)
		if self.application_status=="Approved" and self.docstatus==1:
			student = get_mapped_doc("Student Exchange Applicant", self.name,
				{"Student Exchange Applicant": {
					"doctype": "Student",
					"field_map": {
						"name": "student_exchange_applicant"
					}
				}}, ignore_permissions=True)
			student.save()


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_active_exchange_program_declaration(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(""" select p.name,p.programs_name from `tabExchange Program Declaration` exp
		left join `tabPrograms` p on p.name=exp.program__to_exchange
		where exp.is_active = %(active)s and exp.program__to_exchange like %(txt)s
		limit %(start)s, %(page_len)s""", {
			'active': filters.get("is_active"),
			'start': start,
			'page_len': page_len,
			'txt': "%%%s%%" % txt
		})

@frappe.whitelist()
def get_student_exchange_program(exchange_program,student_category):
	for epd in frappe.get_all("Exchange Program Declaration",{"program__to_exchange":exchange_program,"student_category":student_category}):
		return epd

@frappe.whitelist()
def enroll_student(source_name):
	from kp_edtec.kp_edtec.doctype.semesters.semesters import get_courses
	for st in frappe.get_all("Student",{"student_exchange_applicant":source_name}):
		student=frappe.get_doc("Student",st.name)
		student_exchange_applicant=frappe.get_doc("Student Exchange Applicant",source_name)
		exchange_program_declaration=frappe.get_doc("Exchange Program Declaration",student_exchange_applicant.student_exchange_program)
		program_enrollment = frappe.new_doc("Program Enrollment")
		program_enrollment.student = student.name
		program_enrollment.student_category = student.student_category
		program_enrollment.student_name = student.title
		program_enrollment.reference_doctype="Student Exchange Applicant"
		program_enrollment.reference_name=source_name
		program_enrollment.programs = exchange_program_declaration.program__to_exchange
		program_enrollment.program = exchange_program_declaration.semester
		program_enrollment.academic_year=student_exchange_applicant.academic_year
		program_enrollment.academic_term=student_exchange_applicant.academic_term
		program_enrollment.program_grade=frappe.db.get_value("Programs",{"name":exchange_program_declaration.program__to_exchange},"program_grade")
		if program_enrollment.program:
			for crs in get_courses(program_enrollment.program):
				program_enrollment.append("courses",crs.update({"course":crs.name}))
		if student_exchange_applicant.student_exchange_program:
			academic_template=exchange_program_declaration.academic_calendar_template
			if academic_template:
				for d in get_academic_calender_table(academic_template):
					program_enrollment.append("academic_events_table",d)
		if exchange_program_declaration.fees_applicable=="YES":
			for fs in exchange_program_declaration.get("fee_structure"):
				if fs.student_category==student.student_category:
					program_enrollment.append("fee_structure_item",{
						"student_category":student.student_category,
						"fee_structure":fs.fee_structure,
						"amount":fs.amount,
						"due_date":fs.due_date
					})
		return program_enrollment

@frappe.whitelist()
def show_fees_button( student_exchange_applicant,exchange_program_declaration):
	exchange_program_declaration_doc=frappe.get_doc("Exchange Program Declaration",exchange_program_declaration)
	if exchange_program_declaration_doc.fees_applicable=="YES":
		for st in frappe.get_all("Student",{"student_exchange_applicant":student_exchange_applicant}):
			if len(frappe.get_all("Fees",{"student":st.name}))>0:
				return False
	else:
		return False
	return True

@frappe.whitelist()
def create_fees(source_name, target_doc=None):
	from kp_edtec.kp_edtec.doctype.program_enrollment import get_program_enrollment
	def set_missing_values(source, target):
		for d in frappe.get_all("Student",{"student_exchange_applicant":source.name}):
			target.student=d.name
		for d in frappe.get_all("Exchange Program Declaration",{"name":source.student_exchange_program,"fees_applicable":"YES"},["name","program__to_exchange","semester"]):
			for fsi in frappe.get_all("Fee Structure Item",{"parent":d.name,"parentfield":"fee_structure","parenttype": "Exchange Program Declaration"},["fee_structure"]):
				target.fee_structure=fsi.fee_structure

			target.programs=d.program__to_exchange
			target.program=d.semester
			for fc in frappe.get_all("Fee Component",{"parent":target.fee_structure},['fees_category','amount','description']):
				target.append("components",{
					"fees_category":fc.fees_category,
					"amount":fc.amount,
					"description":fc.description
				})
		if get_program_enrollment(target.student):
			target.program_enrollment=get_program_enrollment(target.student)['name']
		if source.student_exchange_program:
			exchange_program_declaration_doc=frappe.get_doc("Exchange Program Declaration",source.student_exchange_program)
			if exchange_program_declaration_doc.fees_applicable=="YES":
				for d in exchange_program_declaration_doc.get("fee_structure"):
					if source.student_category==d.student_category:
						target.due_date=d.due_date
	
	doclist = get_mapped_doc("Student Exchange Applicant", source_name, 	{
		"Student Exchange Applicant": {
			"doctype": "Fees",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
	}, target_doc,set_missing_values)

	return doclist

@frappe.whitelist()
def get_document_list_by_category(category,year,student_exchange):
	for re_doc in frappe.get_all("Required Documents",{"parent":student_exchange,"student_category":category,"parenttype":"Exchange Program Declaration"},["document_type"]):
			return frappe.get_all("Documents Template List",{"parent":re_doc.document_type},['document_name','mandatory'])
	return []

def get_academic_calender_table(academic_template):
	doc=frappe.get_doc("Academic Calendar Template",academic_template)
	table=[]
	for d in doc.get("academic_events_table"):
		table.append({
			"academic_events":d.academic_events,
			"start_date":d.start_date,
			"end_date":d.end_date,
			"duration":d.duration
		}
		)
	return table

def mobile_number_validation(doc):
	if doc.student_mobile_number:
		if not (doc.student_mobile_number).isdigit():
			frappe.throw("Field <b>Mobile Number</b> Accept Digits Only")
		if len(doc.student_mobile_number)<10:
			frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")

def date_validation(doc):
	if doc.student_exchange_program:
		declaration=frappe.get_doc("Exchange Program Declaration",doc.student_exchange_program)
		if (getdate(declaration.application_end)<getdate(doc.application_date) and getdate(declaration.application_start)<getdate(doc.application_date)) or (getdate(declaration.application_end)>getdate(doc.application_date) and getdate(declaration.application_start)>getdate(doc.application_date)):
			frappe.throw("Application Date Should be in Between Start and End Date of Declaration")

def validate_attachment(doc):
	for d in doc.get("document_list"):
		if (d.mandatory or d.is_available) and not d.attach:
			frappe.throw("Please Attach Document <b>{0}</b>".format(d.document_name))