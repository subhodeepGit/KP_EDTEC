# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address
from frappe.model.mapper import get_mapped_doc

class PlacementCompany(Document):
    def onload(self):
        """Load address and contacts in `__onload`"""
        load_address_and_contact(self)

    def validate(self):
        validate_department(self)

def validate_department(doc):
    for d in doc.belong_to_department:
        if d.department:
            if d.department not in [d.name for d in frappe.get_all("Department", {"is_stream":0},['name'])]:
                frappe.throw("Department <b>'{0}'</b> is not valid".format(d.department))

@frappe.whitelist()
def create_placement_drive(source_name, target_doc=None):
    doclist = get_mapped_doc("Placement Company", source_name,  {
        "Placement Company": {
            "doctype": "Placement Drive",
            "field_map": {
                "company_name": "placement_company"
            },
            "validation": {
                "docstatus": ["!=", 2]
            }
        },
        "Placement Department": {
            "doctype": "Placement Department",
            "field_map": {
                "department": "department"
            }
        }
    }, target_doc)

    return doclist