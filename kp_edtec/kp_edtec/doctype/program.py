import frappe
from kp_edtec.kp_edtec.utils import duplicate_row_validation

def validate(doc,method):
	duplicate_row_validation(doc, "courses", ['course', 'course_name'])
	validate_course(doc)

def on_trash(doc,method):
    validate_course_if_exists(doc)

def validate_course(doc):
	for c in doc.courses:
		if c.course:
			if c.course not in [d.name for d in frappe.get_all("Course", {"disable":0},['name'])]:
				frappe.throw("Course <b>'{0}'</b> not valid".format(c.course))

def after_insert(doc,method):
    if doc.get("programs"):
        programs=frappe.get_doc("Programs",doc.get("programs"))
        if doc.program_name not in [d.semesters for d in programs.get("semesters")]:
            programs.append("semesters",{
                "semesters":doc.name,
                "semesters_name":doc.program_name
            })
            programs.no_of_semesters=len(programs.semesters)
            programs.save()

def validate_course_if_exists(doc):
    if len(doc.get("courses"))!=0:
        frappe.throw("Please Delete Courses from Semester")