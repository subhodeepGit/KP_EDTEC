import frappe
from kp_edtec.ed_tec.validations.student_admission import validate_academic_year
from kp_edtec.ed_tec.validations.course import validate_semester
from kp_edtec.ed_tec.utils import get_courses_by_semester

def validate(doc, method):
    validate_academic_year(doc)
    validate_semester(doc)
    validate_student(doc)
    validate_course_assessment_plan(doc)
    validate_course(doc)

def validate_student(doc):
    if doc.get('student_group') and doc.student not in [d.student for d in frappe.get_all("Student Group Student",{"parent":doc.get("student_group")},["student"])]:
        frappe.throw("Student <b>'{0}'</b> not belongs to student group <b>'{1}'</b> ".format(doc.get('student'),doc.get('student_group') ))

def validate_course_assessment_plan(doc):
    if doc.course_assessment_plan not in [d.name for d in frappe.get_all("Course Assessment Plan", {'docstatus': 1},['name'])]:
        frappe.throw("Course assessment plan <b>'{0}'</b> should be docstatus 1".format(doc.get('course_assessment_plan')))

def validate_course(doc):
    for a in doc.assessment_result_item:
        if a.course :
            if a.course not in get_courses_by_semester(doc.program):
                frappe.throw("Course <b>'{0}'</b> not belongs to program <b>'{1}'</b> ".format(a.get('course'),doc.get('program') ))
    for a in doc.course_final_result:
        if a.course :
            if a.course not in get_courses_by_semester(doc.program):
                frappe.throw("Course <b>'{0}'</b> not belongs to program <b>'{1}'</b> ".format(a.get('course'),doc.get('program') ))
    if doc.course:
        if doc.course not in get_courses_by_semester(doc.program):
            frappe.throw("Course <b>'{0}'</b> not belongs to program <b>'{1}'</b> ".format(doc.get('course'),doc.get('program') ))
