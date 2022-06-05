import frappe

def validate(doc, method):
    validate_program(doc)

def validate_program(doc):
    dept=frappe.db.get_value("Programs",{"name":doc.get("for_program")},"department")
    if dept:
        for b in doc.branch_sliding__criteria:
            if b.program:
                if b.program not in [p['name'] for p in frappe.get_all("Programs", {'department':dept},['name'])]:
                    frappe.throw("Program <b>'{0}'</b> not belongs to same department of program <b>'{1}'</b> ".format(doc.get('for_program'),b.program))
                if b.semester:
                    if b.semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':b.program},['semesters'])]:
                        frappe.throw("Semester <b>'{0}'</b> not belongs to program <b>'{1}'</b> ".format(b.semester,b.program))
