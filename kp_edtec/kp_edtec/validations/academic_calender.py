import frappe

def validate(doc, method):
	validate_academic_calender_template(doc)

def validate_academic_calender_template(doc):
	template_list = [d.name for d in frappe.get_all("Academic Calendar Template", {'programs':doc.get('program'),"academic_year": doc.academic_year},['name'])]
	if doc.get('academic_calendar_template') not in template_list:
		frappe.throw("Academic calender template <b>'{0}'</b> not belongs to program <b>'{1}'</b>".format(doc.get('academic_calendar_template'), doc.get('program')))