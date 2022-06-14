# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc

class HostelAdmission(Document):
	@frappe.whitelist()
	def get_missing_fields(self):
		student=frappe.get_doc("Student",self.student)

		self.set("guardians_list",[])
		for gr in student.get("guardians"):
			self.append("guardian_list",{
				"guardian":gr.guardian,
				"guardian_name":gr.guardian_name,
			})

		for cr_ed in student.get("current_education"):
			self.programs=cr_ed.programs
			self.academic_year=cr_ed.academic_year
	   
	# def on_submit(self):
	#     if self.hostel_fee_structure:
	#         create_fees(self)

@frappe.whitelist()
def create_fees(source_name, dialog_value,target_doc=None):
	dialog_value=json.loads(dialog_value)
	def set_missing_values(source, target):
		fee_comp = frappe.db.get_all("Fee Component", {'parent':dialog_value['fee_structure']}, ['fees_category', 'amount'])
		for fee in fee_comp:
			comp_row = target.append('components', {})
			comp_row.fees_category = fee.fees_category
			comp_row.amount = fee.amount
		if source.programs:
			semester = [i.get('program') for i in frappe.db.get_all("Program Enrollment", {'programs':source.programs, 'student': source.student, "docstatus":1}, 'program')]   
			target.program = semester[0]
	doclist = get_mapped_doc("Hostel Admission", source_name,  {
		"Hostel Admission": {
			"doctype": "Fees",
			"field_map": {
				"programs":"programs",
				"student":"student",
				"due_date":"due_date",
				"name" : "hostel_admission"
			},
		},
	}, target_doc,set_missing_values)
	doclist.valid_from=dialog_value['from_date']
	doclist.valid_to=dialog_value['to_date']
	doclist.fee_structure=dialog_value['fee_structure']
	doclist.save()
	return doclist
