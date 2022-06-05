# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProvisionalCertificate(Document):
	@frappe.whitelist()
	def get_missing_fields(self):
		data={}
		data["prn"]=frappe.db.get_value("Student",self.student,"permanant_registration_number")
		data["programs"]=frappe.db.get_value("Current Educational Details",{"parent":self.student},"programs")
		return data