import frappe
from kp_edtec.kp_edtec.validations.course import validate_semester
from kp_edtec.kp_edtec.validations.program_enrollment import validate_student

def validate(doc, method):
	if doc.program:
		validate_semester(doc)
	validate_student_group(doc)
	validate_student(doc)
	validate_faculty(doc)

def validate_student_group(doc):
	if doc.student_group:
		if doc.student_group not in [d.name for d in frappe.get_all("Student Group", {'programs':doc.get('programs')},['name'])]:
			frappe.throw("Student Group <b>'{0}'</b> not belongs to programs <b>'{1}'</b>".format(doc.get('student_group'), doc.get('programs')))

def validate_faculty(doc):
	if doc.faculty:
		if doc.faculty not in [d.parent for d in frappe.get_all("Instructor Log", {'student_group':doc.get('student_group')},['parent'])]:
			frappe.throw("Student Group <b>'{0}'</b> not belongs to faculty <b>'{1}'</b>".format(doc.get('student_group'), doc.get('faculty')))
