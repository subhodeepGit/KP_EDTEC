import frappe

def validate(doc, method):
	validate_semester(doc)
	validate_students(doc)

def validate_semester(doc):
	if doc.semester and doc.program:
		if doc.semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('program')},['semesters'])]:
			frappe.throw("Semester <b>'{0}'</b> not belongs to programs <b>'{1}'</b>".format(doc.get('semester'), doc.get('program')))

def validate_students(doc):
	if doc.semester and doc.program:
		for m in doc.mentee_list:
			if m.student not in [d.parent for d in frappe.get_all("Current Educational Details", {'programs':doc.get('program'),'semesters':doc.get('semester')},['parent'])]:
				frappe.throw("Student <b>'{0}'</b> not belongs to programs <b>'{1}'</b> and semester <b>'{2}'</b>".format(m.student, doc.get('program'),doc.get('semester') ))

	for ma in frappe.get_all("Mentor Allocation",{"allocation_from":doc.allocation_from,"allocation_to":doc.allocation_to,"docstatus":1,"name":("!=",doc.name)}):
		for student in doc.get("mentee_list"):
			if student.student in [d.student for d in frappe.get_all("Mentee List",{"parent":ma.name},['student'])]:
				frappe.throw("Student <b>{0}</b> already Exists in Mentor Allocation <b>{1}</b>".format(student.student,ma.name))
