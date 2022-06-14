# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate

class HostelRoom(Document):
	def validate(self):
		self.set_seat_balance_if_no_allotment()
		# self.validate_room_no()
		self.validate_capacity_and_balance()

	def after_insert(self):
		building_doc = frappe.get_doc("Building", self.building)
		building_doc.total_rooms += 1
		building_doc.save()


	def set_seat_balance_if_no_allotment(self):
		if len(frappe.get_all("Allotment  Ledger",{"hostel_room":self.name}))==0:
			self.seat_balance=self.total_capacity

	@frappe.whitelist()
	def create_allotment_ledger(self):
		data=frappe.new_doc("Allotment  Ledger")
		data.hostel_room = self.name
		data.allotment_type = self.seat_type
		data.allotment_date = today()
		data.no_of_beds = self.seats
		data.reference_doctype = "Hostel Room"
		data.reference_name = self.name
		data.save()
		return "true"
		

	def validate_room_no(self):
		if isinstance(self.room_number, int):
			pass
		else:
			frappe.throw("Room number should be integer")

	def validate_capacity_and_balance(self):
		if self.total_capacity < self.seat_balance:
			frappe.throw("Seat Balance should be less than Total Capacity")
		 
		if self.seat_balance<0:
			frappe.throw("Seat Balance Cannot be Negative")

def update_seat_balance(doc):
	allocated_beds = frappe.db.sql("""select sum(no_of_beds) as beds from `tabAllotment  Ledger` where hostel_room='{0}'""".format(doc.name), as_dict=1)
	if allocated_beds and doc.seat_balance:
		doc.seat_balance = doc.total_capacity - allocated_beds[0]['beds']
