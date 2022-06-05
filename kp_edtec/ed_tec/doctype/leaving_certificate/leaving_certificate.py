# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeavingCertificate(Document):
    @frappe.whitelist()
    def get_missing_fields(self):
        data={}
        data["enrollment_dte"]=frappe.db.get_value("Program Enrollment",{"student":self.student,"docstatus":1},"enrollment_date")
        data["prn"]=frappe.db.get_value("Program Enrollment",{"student":self.student,"docstatus":1},"permanant_registration_number","enrollment_date")
        data["guardian"]=frappe.db.get_value("Student Guardian",{"parent":self.student},"guardian_name")
        data["class"]=frappe.db.get_value("Current Educational Details",{"parent":self.student},"programs")
        stud_data =frappe.get_all("Student",{"name":self.student},["address_line_1","address_line_2", "date_of_birth", "pin_code","mothers_name", "fathers_name", "city", "police_station", "post_office","district", ])
        stud_data = stud_data[0] if stud_data[0] else ''
        if stud_data["address_line_1"] :
            if stud_data["address_line_2"] :
                data["address"] = stud_data["address_line_1"] +', '+ stud_data["address_line_2"]
            else:
                data["address"] = stud_data["address_line_1"]
        else:
            data["address"] = stud_data["address_line_2"] 
        data['date_of_birth'] = stud_data['date_of_birth']
        data['pincodex'] = stud_data['pin_code'] 
        data['father_name'] = stud_data['fathers_name']
        data['mothers_name'] = stud_data['mothers_name'] 
        data['village'] = stud_data['city']
        data['police_station'] = stud_data['police_station']
        data['post_office'] = stud_data['post_office'] 
        data['district'] = stud_data['district']
        return data
