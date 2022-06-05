import frappe

def validate(doc, method):
    validate_semester(doc)
    validate_max_credit(doc)

def validate_semester(doc):
    if  doc.program and doc.programs:
        if doc.program not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('programs')},['semesters'])]:
            frappe.throw("Semester <b>'{0}'</b> not belongs to program <b>'{1}'</b>".format(doc.get('program'), doc.get('programs')))

def validate_max_credit(doc):
    total_credit = 0
    if doc.total_credit:
        for cd in doc.credit_distribution:
           if cd.passing_marks > cd.total_marks:
               frappe.throw("Passing marks <b>{0}</b> should not be greater than total marks <b>{1}</b>.".format(cd.passing_marks, cd.total_marks))
           if cd.passing_credits > cd.credits:
               frappe.throw("Passing credits <b>{0}</b> should not be greater than total credits <b>{1}</b>.".format(cd.passing_credits, cd.credits))
           total_credit += cd.credits
        doc.total_credit = total_credit
        if doc.total_credit != total_credit:
            frappe.throw("Credit totals <b>{0}</b> should be match with total credit <b>{1}</b>.".format(total_credit, doc.total_credit))

