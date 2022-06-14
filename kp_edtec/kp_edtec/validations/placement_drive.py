import frappe

def validate(doc, method):
	validate_semester(doc)

def validate_semester(doc):
	for i in doc.for_programs:
		if i.programs:
			dept_list = [d.department for d in frappe.get_all("Placement Department", {'parent':doc.name},['department'])]	
			if dept_list:	
				if i.programs not in [d.name for d in frappe.get_all("Programs", {'department':['in', dept_list]},['name'])]:	
					frappe.throw("Program <b>'{0}'</b> not belongs to departments".format(i.get('programs')))
			if i.semester:
				if i.semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':i.get('programs')},['semesters'])]:
					frappe.throw("Semester <b>'{0}'</b> not belongs to programs <b>'{1}'</b>".format(i.get('semester'), i.get('programs')))