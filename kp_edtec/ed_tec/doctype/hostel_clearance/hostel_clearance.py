# Copyright (c) 2022, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HostelClearance(Document):
	
	@frappe.whitelist()
	def get_hostel_details(self):
			for allotment in frappe.get_all("Hostel Allotment",{"student":self.student,"docstatus":1},["building", "to_room","floor","room_type","name"]):
				return allotment


@frappe.whitelist()
def get_hostel_students(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT distinct student,student_name from `tabHostel Allotment` where docstatus=1 and (student like '%{0}%' or student_name like '%{0}%')""".format(txt))

