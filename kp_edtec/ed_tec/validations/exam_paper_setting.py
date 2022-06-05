import frappe
from kp_edtec.ed_tec.validations.student_admission import validate_academic_year
from kp_edtec.ed_tec.validations.course import validate_semester

def validate(doc, method):
	if doc.academic_year:
		validate_academic_year(doc)
	validate_semester(doc)
	# validate_course(doc)
	# validate_assessment_plan(doc)

def validate_course(doc):
	if doc.examiner:
		courses = frappe.db.sql("""SELECT IL.course from `tabInstructor Log` as IL 
		inner join `tabInstructor` as I on IL.parent=I.name 
		where I.name = '{0}'""".format(doc.examiner), as_dict=1)
		if doc.course:
			if doc.course not in [d.course for d in courses]:
				frappe.throw("Course <b>'{0}'</b> not belongs to examiner <b>'{1}'</b>".format(doc.get('course'), doc.get('examiner')))

def validate_assessment_plan(doc):
	if doc.assessment_plan:
		if doc.assessment_plan not in [d.name for d in frappe.get_all("Course Assessment Plan", {'programs':doc.get('programs'), "program":doc.get('program'),"docstatus":1},['name'])]:
			frappe.throw("Assessment Plan <b>'{0}'</b> not belongs to programs <b>'{1}'</b> and semester <b>'{2}'</b>".format(doc.get('assessment_plan'), doc.get('programs'),doc.get('program')))
