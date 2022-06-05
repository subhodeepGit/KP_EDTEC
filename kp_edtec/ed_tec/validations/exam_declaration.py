import frappe
from kp_edtec.ed_tec.utils import date_greater_than
from kp_edtec.ed_tec.utils import get_courses_by_semester

def validate(doc, method):
	validate_semester(doc)
	validate_fee_structure(doc)

def validate_semester(doc):
	semester_list=[d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('exam_program')},['semesters'])]
	if doc.semesters:
		for d in doc.semesters:
			get_courses_by_semester(d.get('semester'))
			# if d.get('semester') not in semester_list:
			# 	frappe.throw("Semester <b>'{0}'</b> not belongs to Exam Program <b>'{1}'</b>".format(d.get('semester'), doc.get('exam_program')))

def validate_fee_structure(doc):
	for i in doc.fee_structure:
		if i.fee_structure:
			if i.fee_structure not in [d.name for d in frappe.get_all("Fee Structure", {'programs':doc.get('exam_program'),"docstatus":1},['name'])]:
				frappe.throw("Fee structure <b>'{0}'</b> not belongs to program <b>'{1}'</b> ".format(i.fee_structure, doc.get('exam_program')))
