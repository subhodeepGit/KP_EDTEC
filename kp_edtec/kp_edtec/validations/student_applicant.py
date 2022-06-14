import frappe
from kp_edtec.kp_edtec.validations.student_admission import validate_academic_year
from kp_edtec.kp_edtec.utils import duplicate_row_validation

def validate(doc, method):
    validate_counselling_structure(doc)
    validate_academic_year(doc)
    duplicate_row_validation(doc, "guardians", ['guardian', 'guardian_name'])
    duplicate_row_validation(doc, "siblings", ['full_name', 'gender'])
    validate_pincode(doc)

def on_submit(doc, method): 
    for docmnt in doc.document_list:
        if docmnt.attach:
            docmnt.is_available = 1
        else:
            docmnt.is_available = 0

def validate_pincode(doc):
    if doc.pin_code:
        if not check_int(doc.pin_code):
            frappe.throw("Pincode must be the integer.")

def check_int(pin_code):
    import re
    return re.match(r"[-+]?\d+(\.0*)?$", pin_code) is not None

def validate_counselling_structure(doc):
    if doc.counselling_structure:
        if doc.counselling_structure not in [d['name'] for d in frappe.get_all("Counselling Structure",{"program_grade":doc.program_grade,"department":doc.department,"academic_year":doc.academic_year},['name'])]:
            frappe.throw("Counselling structure <b>'{0}'</b> not belongs to program grade,academic year and department".format(doc.counselling_structure))
            
        program_list = [d.programs for d in frappe.get_all("Counselling Programs",{"parent":doc.counselling_structure},"programs")]
        for p in doc.program_priority:
            if program_list and p.programs:
                if p.programs not in program_list:
                    frappe.throw("Programs <b>'{0}'</b> not belongs to Counselling Structure <b>'{1}'</b>".format(p.programs, doc.counselling_structure))
        # parameter_list = frappe.db.get_value("Eligibility Parameter List",{"parent":doc.counselling_structure, 'student_category':doc.student_category},"parameter")
        # parameter_total_list = frappe.db.get_all("Eligibility Parameter List",{"parent":doc.counselling_structure, 'student_category':doc.student_category},["parameter", "total_score"])
        # for p in doc.education_qualifications_details:
        #     if p.qualification:
        #         if p.qualification not in [p['parameter'] for p in parameter_total_list]:
        #             frappe.throw("Qualification of education qualifications details <b>'{0}'</b> not belongs to Counselling Structure <b>'{1}'</b>".format(p.qualification, doc.counselling_structure))
        #         else:
        #             for pt in parameter_total_list:
        #                 if pt.parameter == p.qualification:
        #                     if p.score > pt.total_score:
        #                         frappe.throw("Score <b>'{0}'</b> of education qualifications details should not be greater than the total score <b>'{1}'</b>".format(p.score, pt.total_score))
    # else:
    #     if doc.department and doc.program_grade:
    #         for p in doc.program_priority:
    #             if p.programs:
    #                 if p.programs not in [d['name'] for d in frappe.get_all("Programs",{"program_grade":doc.program_grade,"department":doc.department},['name'])]:
    #                     frappe.throw("Programs <b>'{0}'</b> not belongs to program grade <b>'{1}'</b> and department <b>'{2}'</b>".format(p.programs, doc.program_grade, doc.department))
        # for p in doc.program_priority:
        #     if p.student_admission and doc.student_category:
        #         # parameter_list = [i['parameter'] for i in frappe.db.get_all("Eligibility Parameter List",{"parent":p.student_admission, 'student_category':doc.student_category},["parameter"])]
        #         parameter_total_list = frappe.db.get_all("Eligibility Parameter List",{"parent":p.student_admission, 'student_category':doc.student_category},["parameter", "total_score"])
        #         for e in doc.education_qualifications_details:
        #             if e.qualification not in [p.parameter for p in parameter_total_list]:
        #                 frappe.throw("Qualification of education qualifications details <b>'{0}'</b> not belongs to Student Admission <b>'{1}'</b>".format(e.qualification, p.student_admission))
        #             else:
        #                 for pt in parameter_total_list:
        #                     if pt.parameter == e.qualification:
        #                         if e.score > pt.total_score:
        #                             frappe.throw("Score <b>'{0}'</b> of education qualifications details should not be greater than the total score <b>'{1}'</b>".format(e.score, pt.total_score))
