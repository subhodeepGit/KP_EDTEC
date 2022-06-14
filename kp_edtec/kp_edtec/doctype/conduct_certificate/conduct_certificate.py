# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ConductCertificate(Document):
	@frappe.whitelist()
	def get_missing_fields(self):
	    data={}
	    data["academic_year"]=frappe.db.get_value("Current Educational Details",{"parent":self.student},"academic_year")
	    academic_yr_data  = frappe.get_all("Academic Year", {'name':data["academic_year"]}, ['year_start_date', 'year_end_date'])
	    data['academic_year_start'] = academic_yr_data[0]['year_start_date']
	    data['academic_year_end'] = academic_yr_data[0]['year_end_date']
	    return data
