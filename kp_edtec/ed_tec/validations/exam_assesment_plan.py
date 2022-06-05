import frappe
from kp_edtec.ed_tec.validations.student_admission import validate_academic_year
from kp_edtec.ed_tec.validations.course import validate_semester

def validate(doc, method):
	if doc.academic_year:
		validate_academic_year(doc)
	validate_semester(doc)
	# validate_assessment_group(doc)
	validate_grading_scale(doc)
	# validate_student_group(doc)

# def validate_assessment_group(doc):
# 	if doc.assessment_group :
# 		if doc.assessment_group not in [d.name for d in frappe.get_all("Assessment Group", {'is_group': 0},['name'])]:
# 			frappe.throw("Assessment group <b>'{0}'</b> should be is group 0".format(doc.get('assessment_group')))

def validate_grading_scale(doc):
	if doc.grading_scale not in [d.name for d in frappe.get_all("Grading Scale", {'docstatus': 1},['name'])]:
		frappe.throw("Grading scale <b>'{0}'</b> should be docstatus 1".format(doc.get('grading_scale')))

def validate_student_group(doc):
	if doc.student_group not in [d.name for d in frappe.get_all("Student Group", {"group_based_on":"Exam Declaration"},['name'])]:
		frappe.throw("Student group <b>'{0}'</b> should be group based on Exam Declaration".format(doc.get('student_group')))