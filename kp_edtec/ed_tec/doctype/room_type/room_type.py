# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoomType(Document):
	@frappe.whitelist()
	def set_capacity(self):
		if self.capacity:
			hostel_room_list = [i.name for i in frappe.get_all("Hostel Room", {'room_type':self.name})]
			for h in hostel_room_list:
				hostel_room_doc = frappe.get_doc("Hostel Room",h)
				hostel_room_doc.total_capacity = self.capacity
				hostel_room_doc.save()
