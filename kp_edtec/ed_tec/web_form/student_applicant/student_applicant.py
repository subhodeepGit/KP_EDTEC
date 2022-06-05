from __future__ import unicode_literals

import frappe

def get_context(context):
    # do your magic here
    pass

def has_website_permission(doc, ptype, user, verbose=False):
    if frappe.session.user == 'Guest':
        return True
    else:
        return False

@frappe.whitelist(allow_guest=True)
def get_programs_list(department,program_grade):
    dept_list = [d.name for d in frappe.db.get_list("Department", {'parent_department':department},'name')]
    return frappe.db.get_list("Programs", {'program_grade':program_grade, 'department': ['in', dept_list]},'name')

@frappe.whitelist(allow_guest=True)
def get_phone_code(states):
    country = frappe.db.get_value("State",{"name":states},'country')
    if frappe.db.get_value("Country",{"name":country},'country_phone_code'):
        return frappe.db.get_value("Country",{"name":country},'country_phone_code')
    else:
        return ''

@frappe.whitelist(allow_guest=True)
def get_counselling_structure(programs):
    return frappe.db.get_value("Counselling Programs", {'programs':programs}, 'parent')

@frappe.whitelist(allow_guest=True)
def get_academic_term(academic_year):
    return frappe.db.get_list("Academic Term", {'academic_year':academic_year}, 'name')

@frappe.whitelist(allow_guest=True)
def get_sub_tribe(tribe):
    return frappe.db.get_list("Sub_Tribe", {'tribe':tribe}, ['name','tribe','tribe_name'])

@frappe.whitelist(allow_guest=True)
def get_sub_tribe_name(name):
    return frappe.db.get_value("Sub_Tribe", {'name':name}, 'sub_tribe_name')

@frappe.whitelist(allow_guest=True)
def get_department():
    return frappe.db.get_list("Department", {'is_group':1,  "is_stream": 1}, 'name')

@frappe.whitelist(allow_guest=True)
def get_qualification_list():
    quali_list =  [q.name for q in frappe.db.get_list("Eligibility Parameters", "name", order_by="name")]
    academic_yr_list =  [q.name for q in frappe.db.get_list("Academic Year", "name", order_by="name")]
    return {'qual':quali_list, 'acadmic':academic_yr_list}

@frappe.whitelist(allow_guest=True)
def get_document_list(student_category):
    doc_list  = frappe.db.sql("""SELECT DL.document_name from `tabDocuments Template List` as DL 
    inner join `tabDocuments Template` as D on DL.parent= D.name where D.student_category='{0}'""".format(student_category), as_list=1)
    return doc_list