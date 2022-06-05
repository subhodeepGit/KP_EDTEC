# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import msgprint, _

class Mentor(Document):
    def validate(self):
        create_full_name(self)

def create_full_name(doc):
    if doc.middle_name:
        doc.full_name = doc.salutation +" "+ doc.first_name +" "+ doc.middle_name +" "+ doc.last_name
    else:
        doc.full_name = doc.salutation +" "+ doc.first_name +" "+ doc.last_name

@frappe.whitelist()
def get_instructor_data(instructor):
    emp = frappe.db.get_value("Instructor", {'name': instructor}, 'employee')
    if emp:
        emp_data = frappe.db.get_value("Employee", {'name': emp}, ['user_id', 'company_email', 'personal_email'], as_dict=1)
        return emp_data if emp_data else 0

@frappe.whitelist()
def create_user(doc):
    import json
    doc = json.loads(doc)
    user_doc = frappe.new_doc('User')
    user_doc.email = doc.get('email_id')
    user_doc.first_name = doc.get('first_name')
    user_doc.last_name = doc.get('last_name')
    user_doc.full_name = doc.get('full_name')
    user_doc.add_roles('Mentor')
    user_doc.enabled = 1
    user_doc.save()
    msgprint(_("User created successfully."))
    return True
