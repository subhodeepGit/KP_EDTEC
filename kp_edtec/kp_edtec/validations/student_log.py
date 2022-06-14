import frappe
from kp_edtec.kp_edtec.validations.student_admission import validate_academic_year

def validate(doc, method):
	validate_academic_year(doc)
	validate_semester(doc)
	validate_student_batch(doc)

def validate_semester(doc):
	if doc.program not in [d.program for d in frappe.get_all("Program Enrollment", {'student':doc.get('student'),"docstatus":1},['program'])]:
		frappe.throw("Program <b>'{0}'</b> not belongs to student <b>'{1}'</b>".format(doc.get('program'), doc.get('student')))

def validate_student_batch(doc):
	if doc.student_batch:
		if doc.student_batch not in [d.student_batch_name for d in frappe.get_all("Program Enrollment", {'student':doc.get('student'),"docstatus":1},['student_batch_name'])]:
			frappe.throw("Student Batch <b>'{0}'</b> not belongs to student <b>'{1}'</b>".format(doc.get('student_batch'), doc.get('student')))
