import frappe

def validate(doc, method):
	validate_sliding_in_program(doc)

def validate_sliding_in_program(doc):
	if doc.sliding_in_program not in [p.program for p in frappe.get_all("Branch Sliding Item",{"parent":doc.get("branch_sliding_declaration")},['program'])]:
		frappe.throw("Sliding in program <b>'{0}'</b> not belongs to branch sliding declaration <b>'{1}'</b>".format(doc.get('sliding_in_program'), doc.get('branch_sliding_declaration')))