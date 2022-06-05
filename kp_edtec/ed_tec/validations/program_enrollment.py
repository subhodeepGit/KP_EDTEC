import frappe
from datetime import date
from kp_edtec.ed_tec.validations.course import validate_semester
from kp_edtec.ed_tec.validations.student_admission import validate_academic_year
from kp_edtec.ed_tec.utils import get_courses_by_semester, duplicate_row_validation

    
def validate(doc, method):
    validate_semester(doc)
    # validate_student(doc)
    validate_program_enrollment(doc)
    validate_academic_year(doc)
    validate_student_category(doc)
    validate_courses(doc)
    validate_dates_on_academic_events(doc)
    validate_seat_reservation_type(doc)
    duplicate_row_validation(doc, "courses", ['course', 'course_name'])
    duplicate_row_validation(doc, "academic_events_table", ['academic_events', 'start_date','end_date'])

def validate_student(doc):
    if doc.programs not in [d.programs for d in frappe.get_all("Current Educational Details", {'parent':doc.get('student')},['programs'])]:
        frappe.throw("Student <b>'{0}'</b> not belongs to programs <b>'{1}'</b>".format(doc.get('student'), doc.get('programs')))

def validate_student_category(doc):
    if doc.student_category:
        if doc.student_category not in [d.student_category for d in frappe.get_all("Student", {'name':doc.get('student')},['student_category'])]:
            frappe.throw("Student Category <b>'{0}'</b> not belongs to student <b>'{1}'</b>".format(doc.get('student_category'), doc.get('student')))

def validate_courses(doc):
    for i in doc.courses:
        if i.course:
            if i.course not in get_courses_by_semester(doc.program):
                frappe.throw("Course <b>'{0}'</b> not belongs to semester <b>'{1}'</b> ".format(i.course, doc.get('program')))

def validate_dates_on_academic_events(doc):
    for i in doc.academic_events_table:
        if i.end_date and i.start_date:
            if i.end_date < i.start_date:
                frappe.throw("End Date <b>'{0}'</b> Should be Greater than Start Date <b>'{1}'</b> in Academic Events Table".format(i.end_date, i.start_date))
            # if f'{date.today():%Y-%m-%d}' > i.start_date:
            #     frappe.throw("Start Date <b>'{0}'</b> in Academic Events Table Should not be less than today's date".format(i.start_date))

def validate_program_enrollment(doc):
    filters = {'academic_year':doc.academic_year, 'programs': doc.programs, "program":doc.program, "student":doc.student,"docstatus":1}
    if doc.academic_term :
        filters.update({"academic_term":doc.academic_term})
    existed_enrollment = [p.name for p in frappe.get_all('Program Enrollment', filters, ["name"])]
    if len(existed_enrollment) > 0:
        for e in existed_enrollment:
            if e:
                frappe.throw("Student <b>'{0}'</b> had program enrollment <b>'{1}'</b> already".format(e.student, e.name))
 
def validate_seat_reservation_type(doc):
    if doc.reference_doctype == "Student Applicant" and doc.reference_name:
        reservation_type=[]
        for i in frappe.get_all("Student Applicant",{"name":doc.reference_name,"docstatus":1},['student_admission','physically_disabled','award_winner']):
            for d in frappe.get_all("Reservations List",{"parent":i.get("student_admission")},['seat_reservation_type']):
                if d.seat_reservation_type=="Physically Disabled":
                    if i.physically_disabled:
                        reservation_type.append(d.seat_reservation_type)
                elif d.seat_reservation_type=="Sport Person":
                    if i.award_winner:
                        reservation_type.append(d.seat_reservation_type)
                else:
                    reservation_type.append(d.seat_reservation_type)
        if doc.seat_reservation_type not in reservation_type:
            frappe.throw("Seat reservation type <b>'{0}'</b> not belongs to the student admission referring doc student applicant <b>'{1}'</b> ".format(doc.seat_reservation_type, doc.reference_name))
