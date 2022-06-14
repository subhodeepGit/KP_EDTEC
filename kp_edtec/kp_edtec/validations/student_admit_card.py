import frappe
from kp_edtec.kp_edtec.validations.student_admission import validate_academic_year

def validate(doc, method):
	validate_academic_year(doc)
	# validate_current_semester(doc)

def validate_current_semester(doc):
	if doc.current_semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('current_program')},['semesters'])]:
		frappe.throw("Current semester <b>'{0}'</b> not belongs to current program <b>'{1}'</b>".format(doc.get('current_semester'), doc.get('current_program')))
