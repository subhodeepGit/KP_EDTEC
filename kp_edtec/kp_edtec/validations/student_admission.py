import frappe
import collections
from collections import Counter


def validate(doc, method):
    validate_program_grade(doc)
    # validate_academic_year(doc)
    validate_semester(doc)
    validate_fee_structure_in_hostel_fees(doc)
    validate_fee_structure_in_counselling(doc)
    validate_fee_structure_in_admission(doc)
    validate_academic_calender(doc)
    validate_counselling_structure(doc)
    validate_admission_program(doc)
    validate_total_seats(doc)
    validate_eligibility_parameters(doc)
    validate_document_type(doc)

def validate_total_seats(doc):
    total_seats = 0
    if len(doc.reservations_distribution) > 0:
        a = [s.seat_reservation_type for s in doc.reservations_distribution]
        seat_reservation_type_list = [d for d, count in collections.Counter(a).items() if count > 1]
        if seat_reservation_type_list: 
            frappe.throw("Duplicate Seat Reservations type in Reservations Distributions.")
    for rd in doc.reservations_distribution:
        if rd.allocated_seat:
            total_seats += rd.allocated_seat
            if rd.seat_balance > rd.allocated_seat:
                frappe.throw("Seats balance should be less than or equal to allocated seats for")
    if doc.total_seats < total_seats and doc.total_seats > 0:
        frappe.throw("Totals of allocated seats should be less than or equal to total seats")
    elif doc.total_seats < 0:
        frappe.throw("Total Seats should not be less than zero")

def validate_eligibility_parameters(doc):
    #duplicate row validation
    if len(doc.eligibility_parameter_list) > 0:
        dataList = []
        for e in doc.eligibility_parameter_list:
            row = {}
            row.update({'student_category':e.student_category, 'parameter':e.parameter})
            dataList.append(row)
        res_list = [i for n, i in enumerate(dataList) if i not in dataList[n + 1:]]
        if len(res_list) < len(dataList):
            frappe.throw("Duplicate row in Eligibility Parameter List.")

    for eligibility in doc.get("eligibility_parameter_list"):
        # negative value
        if eligibility.total_score < 0 or eligibility.eligible_score < 0:
            frappe.throw("Score Value Must be <b>Positive</b> In  {0}".format(doc.doctype))

        # total value should be greater
        if eligibility.total_score < eligibility.eligible_score:
            frappe.throw("<b>Eligible Score</b>  Should be Less than or Equal to <b>Total Score</b> In {0}".format(doc.doctype))


def validate_admission_program(doc):
    if doc.counselling_structure and doc.admission_program:
        if doc.admission_program not in [d.programs for d in frappe.get_all("Counselling Programs", {"parent":doc.counselling_structure},['programs'])]:
            frappe.throw("Admission program <b>'{0}'</b> not belongs to counselling structure <b>'{1}'</b> ".format(doc.admission_program, doc.counselling_structure))

def validate_counselling_structure(doc):
    if doc.counselling_structure:
        if doc.counselling_structure not in [d.name for d in frappe.get_all("Counselling Structure", {"program_grade":doc.program_grade},['name'])]:
            frappe.throw("Counselling Structure <b>'{0}'</b> not belongs to program grade <b>'{1}'</b> ".format(doc.counselling_structure, doc.program_grade))

def validate_academic_calender(doc):
    if doc.academic_calendar:
        if doc.academic_calendar not in [d.name for d in frappe.get_all("Academic Calendar Template", { "programs":doc.admission_program,
                        "program":doc.semester},['name'])]:
            frappe.throw("Academic Calendar <b>'{0}'</b> not belongs to program <b>'{1}'</b> and semester <b>'{2}'</b>".format(doc.get('academic_calendar'), doc.get('admission_program'),doc.get('semester')))

def validate_program_grade(doc):
    if doc.admission_program not in [d.name for d in frappe.get_all("Programs", {'program_grade':doc.get('program_grade')},['name'])]:
        frappe.throw("Admission Program <b>'{0}'</b> not belongs to program grade <b>'{1}'</b>".format( doc.get('admission_program'),doc.get('program_grade')))

def validate_semester(doc):
    if doc.semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('admission_program')},['semesters'])]:
        frappe.throw("Semester <b>'{0}'</b> not belongs to program <b>'{1}'</b>".format(doc.get('semester'), doc.get('admission_program')))

def validate_academic_year(doc):
    if doc.academic_term:
        if doc.academic_term not in [d.name for d in frappe.get_all("Academic Term", {'academic_year':doc.get('academic_year')},['name'])]:
            frappe.throw("Academic Term <b>'{0}'</b> not belongs to academic year <b>'{1}'</b>".format(doc.get('academic_term'), doc.get('academic_year')))

def validate_fee_structure_in_hostel_fees(doc):
    for i in doc.hostel_fees_:
        if i.fee_structure:
            if i.fee_structure not in [d.name for d in frappe.get_all("Fee Structure", {'programs':doc.get('admission_program'),"docstatus":1},['name'])]:
                frappe.throw("Fee structure <b>'{0}'</b> not belongs to program <b>'{1}'</b> in hostel fees".format(i.fee_structure, doc.get('admission_program')))

def validate_fee_structure_in_counselling(doc):
    for i in doc.counselling_fee_structures:
        if i.fee_structure:
            if i.fee_structure not in [d.name for d in frappe.get_all("Fee Structure", {"fee_type":"Counselling Fees",'programs':doc.get('admission_program'),"docstatus":1},['name'])]:
                frappe.throw("Fee structure <b>'{0}'</b> not belongs to program <b>'{1}'</b> in counselling fee structures".format(i.fee_structure, doc.get('admission_program')))

def validate_fee_structure_in_admission(doc):
    for i in doc.admission_fee_structure:
        if i.fee_structure:
            if i.fee_structure not in [d.name for d in frappe.get_all("Fee Structure", {"fee_type":"Admission",'programs':doc.get('admission_program'),"docstatus":1},['name'])]:
                frappe.throw("Fee structure <b>'{0}'</b> not belongs to program <b>'{1}'</b> in admission fee structures".format(i.fee_structure, doc.get('admission_program')))

def validate_document_type(doc):
    if len(doc.required_documents_list) > 0:
        dataList = []
        for i in doc.required_documents_list:
            if i.document_type:
                if i.document_type not in [d.name for d in frappe.get_all("Documents Template", {"is_active":1},['name'])]:
                    frappe.throw("Document type <b>'{0}'</b> is not active.".format(i.document_type))
                #duplicate row validation
                row = {}
                row.update({'student_category':i.student_category, 'document_type':i.document_type})
                dataList.append(row)
        res_list = [i for n, i in enumerate(dataList) if i not in dataList[n + 1:]]
        if len(res_list) < len(dataList):
            frappe.throw("Duplicate row in Required Documents List.")