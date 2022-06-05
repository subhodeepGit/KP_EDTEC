# Copyright (c) 2022, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TransferCertificate(Document):
	@frappe.whitelist()
	def get_missing_fields(self):
		data={}
		data["enrollment_dte"]=frappe.db.get_value("Program Enrollment",{"student":self.student,"docstatus":1},"enrollment_date")
		data["prn"]=frappe.db.get_value("Program Enrollment",{"student":self.student,"docstatus":1},"permanant_registration_number","enrollment_date")
		data["class"]=frappe.db.get_value("Current Educational Details",{"parent":self.student},"programs")
		return data