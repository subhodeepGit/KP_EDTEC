# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address
from kp_edtec.ed_tec.utils import duplicate_row_validation

class DisciplinaryComplaints(Document):
    def onload(self):
        """Load address and contacts in `__onload`"""
        load_address_and_contact(self)

    def validate(self):
        self.validate_fields()
        duplicate_row_validation(self, "guardian_name",['guardian','guardian_name',])
        duplicate_row_validation(self, "discipline_committee",['committee_member'])

    def on_update_after_submit(self):
        duplicate_row_validation(self, "discipline_committee",['committee_member'])

    def validate_fields(self):
        data={}
        for allotment in frappe.get_all("Hostel Allotment",{"student":self.student,"docstatus":1},["building", "to_room","name"]):
            data.update(allotment)
            break
        for allocation in frappe.get_all("Mentee List",{"student":self.student},["parent"]):
            for d in frappe.get_all("Mentor Allocation",{"name":allocation.parent,"docstatus":1},["mentor","mentor_name"]):
                data.update(d)
            break

        if self.mentor and data.get("mentor") and self.mentor != data.get("mentor"):
            frappe.throw("Please Select valid <b>Mentor</b>")

        if self.building and data.get("building") and self.building != data.get("building"):
            frappe.throw("Please Select valid <b>Building</b>")

        if self.room_number and data.get("to_room") and self.room_number != data.get("to_room"):
            frappe.throw("Please Select valid <b>Room Number</b>")  

        if self.student:
            for d in self.guardian_name:
                if d.guardian not in [d.guardian for d in frappe.get_all("Student Guardian",{"parent":self.student},["guardian"])]:
                    frappe.throw("Guardian '{0}' Not Belongs To Student".format(d.guardian))

    @frappe.whitelist()
    def get_student_details(self):
        for allotment in frappe.get_all("Hostel Allotment",{"student":self.student,"docstatus":1},["building", "to_room","name"],limit=1):
            self.building=allotment.building
            self.room_number=allotment.to_room
        for allocation in frappe.get_all("Mentee List",{"student":self.student},["parent"],limit=1):
            for d in frappe.get_all("Mentor Allocation",{"name":allocation.parent,"docstatus":1},["mentor","mentor_name"]):
                self.mentor=d.mentor
                self.mentor_name=d.mentor_name

        student=frappe.get_doc("Student",self.student)

        self.set("guardian_name",[])
        for gr in student.get("guardians"):
            self.append("guardian_name",{
                "guardian":gr.guardian,
                "guardian_name":gr.guardian_name,
                "relation":gr.relation
            })

        for cr_ed in student.get("current_education"):
            self.programs=cr_ed.programs

@frappe.whitelist()
def create_mentor_mentee_communication(source_name, target_doc=None):       
    def set_missing_values(source, target):
        print("*********************")
        # for d in frappe.get_all("Counselling Structure",{"name":source.counselling_structure}):
        #   for fsi in frappe.get_all("Fee Structure Item",{"parent":d.name,"parentfield":"counselling_fees","student_category":source.student_category},["fee_structure","due_date"]):
        #       target.fee_structure=fsi.fee_structure
        #       target.due_date=fsi.due_date
    
    doclist = get_mapped_doc("Disciplinary Complaints", source_name,  {
        "Disciplinary Complaints": {
            "doctype": "Mentor Mentee Communication",
        },
    }, target_doc,set_missing_values)
    return doclist