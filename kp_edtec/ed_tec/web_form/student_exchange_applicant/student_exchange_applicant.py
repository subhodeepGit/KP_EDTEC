from __future__ import unicode_literals

import frappe

def get_context(context):
	# do your magic here
	pass
@frappe.whitelist(allow_guest=True)
def get_document_list(student_category):
    doc_list  = frappe.db.sql("""SELECT DL.document_name from `tabDocuments Template List` as DL 
    inner join `tabDocuments Template` as D on DL.parent= D.name where D.student_category='{0}'""".format(student_category), as_list=1)
    return doc_list

@frappe.whitelist(allow_guest=True)
def get_qualification_list():
    quali_list =  [q.name for q in frappe.db.get_list("Eligibility Parameters", "name", order_by="name")]
    academic_yr_list =  [q.name for q in frappe.db.get_list("Academic Year", "name", order_by="name")]
    return {'qual':quali_list, 'acadmic':academic_yr_list}
