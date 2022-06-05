# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from kp_edtec.ed_tec.utils import duplicate_row_validation

class CounsellingStructure(Document):
	def validate(self):
		self.validate_program_grade()
		self.duplicate_structure()
		duplicate_row_validation(self,"required_documents",['document_type'])
		# validate_student_admission(doc)

	def validate_program_grade(self):
		for i in self.counselling_programs:
			if i.programs not in  [d.name for d in frappe.get_all("Programs", {'program_grade':self.get('program_grade')},['name'])]:
				frappe.throw("Counselling programs <b>'{0}'</b> not belongs to program grade <b>'{1}'</b>".format( i.programs,self.get('program_grade')))

	def duplicate_structure(self):
		for d in frappe.get_all("Counselling Structure",{"program_grade":self.program_grade,"department":self.department,"academic_year":self.academic_year,"name":("!=",self.name)}):
			frappe.throw("Counselling Structure Already Exists")

# def validate_student_admission(doc):
# 	for i in doc.counselling_admission:
# 		couns_admi_data = frappe.db.sql("""SELECT CA.student_admission, CS.name from `tabCounselling Admission` as CA inner join `tabCounselling Structure`  as CS on CA.parent = CS.name where CS.academic_year = '{0}'""".format(doc.academic_year), as_dict=1)
# 		if i.student_admission in [d.student_admission for d in couns_admi_data]:
# 			exist_data = ', '.join(map(str, [d.name for d in couns_admi_data]))
# 			frappe.throw("Student admission <b>'{0}'</b> already exists in Counselling Structure <b>'{1}'</b> ".format(i.student_admission, exist_data))

@frappe.whitelist()
def create_student_admission(source_name, target_doc=None):
	doclist = get_mapped_doc("Counselling Structure", source_name, 	{
		"Counselling Structure": {
			"doctype": "Student Admission",
			"field_map": {
				"start_date": "admission_start_date",
				"end_date": "admission_end_date"
			},
			"validation": {
				"docstatus": ["!=", 2]
			}
		},
	}, target_doc)

	return doclist

@frappe.whitelist()
def filter_programs_by_department(doctype, txt, searchfield, start, page_len, filters):
    # parent_dept = frappe.db.get_value('Department', {'name':filters.get("department")},'parent_department')
    return frappe.get_all("Programs",{"department":["IN",[d.name for d in frappe.get_all("Department",{"parent_department":filters.get("department")})]],'name': ['like', '%{}%'.format(txt)], 'program_grade':filters.get('program_grade')},as_list=1)
