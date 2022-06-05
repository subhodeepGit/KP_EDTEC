import frappe

def validate(doc, method):
    validate_course(doc)

def validate_course(doc):
    for c in doc.courses:
        if c.course:
            if c.course not in [d.name for d in frappe.get_all("Course", {"disable":0},['name'])]:
                frappe.throw("Course <b>'{0}'</b> not valid".format(c.course))


