import frappe

def validate(doc, method):
	validate_students(doc)

@frappe.whitelist()
def validate_students(doc):
	if doc.student and doc.mentor: 
	    for d in frappe.get_all("Mentor Allocation",{"mentor":doc.get("mentor")},["name"]):
	        if doc.student not in [m.student for m in frappe.get_all("Mentee List",{"parent":d.name},['student'])]:
	        	frappe.throw("Student <b>'{0}'</b> not allocated to mentor <b>'{1}'</b>".format(doc.student, doc.mentor))
