import frappe
from frappe import utils
from kp_edtec.ed_tec.utils import semester_belongs_to_programs,academic_term,duplicate_row_validation,get_courses_by_semester

def validate(doc,method):
    validate_instructor_log(doc)
    academic_term(doc)
#     duplicate_row_validation(doc, "instructor_log", ['course'])

def validate_instructor_log(doc):
    for d in doc.get("instructor_log"):
        # validate_academic_year(d)
        validate_semester(d)
        validate_course(d)

def validate_academic_year(doc):
	if doc.academic_term not in [d.name for d in frappe.get_all("Academic Term", {'academic_year':doc.get('academic_year')},['name'])]:
		frappe.throw("Academic Term <b>'{0}'</b> not belongs to academic year <b>'{1}'</b>".format(doc.get('academic_term'), doc.get('academic_year')))

def validate_semester(doc):
	if doc.program not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('programs')},['semesters'])]:
		frappe.throw("Semester <b>'{0}'</b> not belongs to Programs <b>'{1}'</b>".format(doc.get('program'), doc.get('programs')))

def validate_course(doc):
	if doc.course and doc.course not in get_courses_by_semester(doc.program):
		frappe.throw("Course <b>'{0}'</b> not belongs to Semester <b>'{1}'</b>".format(doc.get('course'), doc.get('program')))
