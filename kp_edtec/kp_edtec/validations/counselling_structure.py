import frappe

def validate(doc, method):
    validate_date(doc)
    validate_fee_structure(doc)
    validate_programs(doc)
    validate_eligibility_parameters(doc)
    validate_department(doc)

def validate_date(doc):
    if doc.end_date and  doc.start_date and doc.end_date < doc.start_date:
        frappe.throw("End Date <b>'{0}'</b> Must Be Greater Than Start Date <b>'{1}'</b>".format(doc.end_date, doc.start_date))

def validate_fee_structure(doc):
    programs_list = [p.programs for p in doc.counselling_programs]
    for b in doc.counselling_fees:
        if b.fee_structure not in [f.name for f in frappe.db.get_list('Fee Structure',{'programs':['IN', programs_list]},['name'])]:
            frappe.throw("Fee structure <b>'{0}'</b> not belongs to Counselling programs".format(b.fee_structure))

def validate_programs(doc):
    for b in doc.counselling_programs:
        if b.programs not in [p['name'] for p in frappe.get_all("Programs", {'program_grade':doc.program_grade, 'department':["IN",[d.name for d in frappe.get_all("Department",{"parent_department":doc.get("department")})]]},['name'])]:
            frappe.throw("Counselling programs <b>'{0}'</b> not belongs to program_grade and department".format(b.programs))

def validate_eligibility_parameters(doc):
    for eligibility in doc.get("eligibility_parameter_list"):
        
        # negative value
        if eligibility.total_score < 0 or eligibility.eligible_score < 0:
            frappe.throw("Score Value Must be <b>Positive</b> In  {0}".format(doc.doctype))

        # total value should be greater
        if eligibility.total_score < eligibility.eligible_score:
            frappe.throw("<b>Eligible Score</b>  Should be Less than or Equal to <b>Total Score</b> In {0}".format(doc.doctype))


def validate_department(doc):
    if doc.department and not frappe.db.get_value("Department",{"is_group":1,"is_stream": 1,"name":doc.department}):
        frappe.throw("Department Should be <b>Is Group</b> and <b>Is Stream</b>")