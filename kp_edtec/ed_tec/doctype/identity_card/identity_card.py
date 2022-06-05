# Copyright (c) 2022, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IdentityCard(Document):
	@frappe.whitelist()
	def get_missing_fields(self):
	    data={}
	    # data["prn"]=frappe.db.get_value("Program Enrollment",{"student":self.student,"docstatus":1},"permanant_registration_number")
	    edu_data =frappe.get_all("Current Educational Details",{"parent":self.student},["academic_year", "programs"])
	    data["programs"]= edu_data[0]['programs'] if edu_data[0]['programs'] else ""
	    data["academic_year"] = edu_data[0]['academic_year'] if edu_data[0]['academic_year'] else ""
	    return data
