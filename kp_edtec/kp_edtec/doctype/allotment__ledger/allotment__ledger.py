# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AllotmentLedger(Document):
	def after_insert(self):
		self.update_room_seats()

	def update_room_seats(self):
		room=frappe.get_doc("Hostel Room",self.hostel_room)
		if self.allotment_type=="Add Balance":
			room.seat_balance+=self.no_of_beds
		else:
			room.seat_balance-=self.no_of_beds
		room.save()
		# room.reload()
