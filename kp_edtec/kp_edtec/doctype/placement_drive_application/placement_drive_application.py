# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PlacementDriveApplication(Document):
    def validate(self):
        self.validate_block_student()
        self.validate_placement_drive()

    def on_submit(self):
        self.update_status()
    
    def update_status(self):
        self.status = "Applied"

    def validate_block_student(self):
        if frappe.db.count("Placement Drive Application",{"status":"Hired","docstatus":1,"block_student":1,"student":self.student,"name":("!=",self.name)}):
            frappe.throw("Student is not applicable to fill the the placement drive application")

        is_placement_blocked_student(self)

        
    def validate_placement_drive(self):
        placement_drive=[d.name for d in frappe.db.sql("""select dr.name from `tabPlacement Drive` dr 
                        left join `tabPlace Eligible Programs` dr_item on dr_item.parent=dr.name
                        left join `tabCurrent Educational Details` cr_ed on cr_ed.semesters=dr_item.semester
                        where  cr_ed.parent='{0}' and dr.docstatus=1 """.format(self.get("student")),as_dict=1)]

        if self.placement_drive not in placement_drive:
            frappe.throw("<b>Student</b> not belongs to <b>Placement Drive</b>")
        
@frappe.whitelist()
def get_placement_drive(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""select dr.name from `tabPlacement Drive` dr 
                        left join `tabPlace Eligible Programs` dr_item on dr_item.parent=dr.name
                        left join `tabCurrent Educational Details` cr_ed on cr_ed.programs=dr_item.programs
                        where  cr_ed.parent='{0}' and dr.docstatus=1 and (dr.name like %(txt)s)""".format(filters.get("student")),{'txt': '%%%s%%' % txt})

def is_placement_blocked_student(doc):
    for bl_st in frappe.get_all("Placement Blocked Student List",{"student":doc.student},['parent']):
        for drive in frappe.get_all("Block Drive List",{"parent":bl_st.parent,"placement_drive":doc.placement_drive},'placement_drive'):
            frappe.throw("Student is exists in <b>Placement Blocked Student</b> in {0} placement drive.".format(drive.placement_drive))