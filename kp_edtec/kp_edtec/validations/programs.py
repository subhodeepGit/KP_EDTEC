import frappe
# from datetime import date
# from kp_edtec.kp_edtec.validations.course import validate_semester
# from kp_edtec.kp_edtec.validations.student_admission import validate_academic_year

def validate(doc, method):
    validate_programs_abbreviation(doc)
    validate_department(doc)
    # # validate_student(doc)
    # validate_academic_year(doc)
    # validate_student_category(doc)
    # validate_courses(doc)
    # validate_dates_on_academic_events(doc)

def validate_programs_abbreviation(doc):
    doc.programs_abbreviation = remove(doc.programs_abbreviation)

def remove(string):
    return "".join(string.split())

def validate_department(doc):
    if doc.department not in [d.name for d in frappe.get_all("Department", {"is_group":0,"is_stream":0},['name'])]:
        frappe.throw("Department <b>'{0}'</b> is not valid".format(doc.get('department')))
