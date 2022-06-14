import frappe
from kp_edtec.kp_edtec.validations.student_admission import validate_academic_year

def validate(doc, method):
	validate_academic_year(doc)
	validate_semester(doc)
	validate_fee_structure(doc)
	validate_date(doc)
	validate_academic_calendar_template(doc)
	validate_document_type(doc)

def validate_date(doc):
	if doc.application_end and  doc.application_start and doc.application_end < doc.application_start:
		frappe.throw("Application End Date <b>'{0}'</b> Must Be Greater Than Application Start Date <b>'{1}'</b>".format(doc.application_end, doc.application_start))

def validate_semester(doc):
	if doc.semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('program__to_exchange')},['semesters'])]:
		frappe.throw("Semester <b>'{0}'</b> not belongs to program to exchange <b>'{1}'</b>".format(doc.get('semester'), doc.get('program__to_exchange')))

def validate_fee_structure(doc):
	for i in doc.fee_structure:
		if i.fee_structure:
			if i.fee_structure not in [d.name for d in frappe.get_all("Fee Structure", {'programs':doc.get('program__to_exchange'),"docstatus":1},['name'])]:
				frappe.throw("Fee structure <b>'{0}'</b> not belongs to program to exchange<b>'{1}'</b> ".format(i.fee_structure, doc.get('program__to_exchange')))
			if i.fee_structure not in [d.name for d in frappe.get_all("Fee Structure", {"fee_type":"Student Exchange Application Fees","docstatus":1},['name'])]:
				frappe.throw("Fee structure <b>'{0}'</b> not belongs to fee type<b>'{1}'</b> ".format(i.fee_structure, "Student Exchange Application Fees"))

def validate_academic_calendar_template(doc):
	if doc.academic_calendar_template:
		if doc.academic_calendar_template not in [d.name for d in frappe.get_all("Academic Calendar Template", {'programs':doc.get('program__to_exchange'), "program":doc.get('semester')},['name'])]:
			frappe.throw("Academic Calendar Template <b>'{0}'</b> not belongs to program to exchange <b>'{1}'</b> and semester <b>'{2}'</b>".format(doc.get('academic_calendar_template'), doc.get('program__to_exchange'),doc.get('semester')))

def validate_document_type(doc):
    for i in doc.required_documents:
        if i.document_type:
            if i.document_type not in [d.name for d in frappe.get_all("Documents Template", {"is_active":1},['name'])]:
                frappe.throw("Document type <b>'{0}'</b> is not active.".format(i.document_type))

