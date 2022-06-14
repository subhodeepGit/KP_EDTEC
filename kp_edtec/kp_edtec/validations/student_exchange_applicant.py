import frappe

def validate(doc, method):
	validate_exchange_program(doc)

def validate_exchange_program(doc):
	if doc.student_exchange_program not in [d.name for d in frappe.get_all("Exchange Program Declaration", {'is_active':1},['name'])]:
		frappe.throw("Exchange program declaration <b>'{0}'</b> is not active.".format(doc.get('student_exchange_program')))