import frappe

def validate(doc, method):
	validate_semester(doc)

def validate_semester(doc):
	if  doc.current_semester and doc.programs:
		if doc.current_semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('programs')},['semesters'])]:
			frappe.throw("Semester <b>'{0}'</b> not belongs to programs <b>'{1}'</b>".format(doc.get('current_semester'), doc.get('programs')))