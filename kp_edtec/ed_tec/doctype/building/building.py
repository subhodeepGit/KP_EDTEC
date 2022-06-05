# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address

class Building(Document):
    def onload(self):
        """Load address and contacts in `__onload`"""
        load_address_and_contact(self)

    def validate(self):
        update_hostel_room(self)

def update_hostel_room(doc):      
    for r in frappe.get_list("Hostel Room", {'building': doc.name}, ["name"]):
        room_doc = frappe.get_doc("Hostel Room", r)
        room_doc.disable = doc.disable 
        if not room_doc.default_room_type:
            room_doc.default_room_type = room_doc.room_type  
        room_doc.save()
        room_doc.reload()