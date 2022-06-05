# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, today

class HostelDeallotment(Document):
	def validate(self):
		self.validate_duplicate()

	@frappe.whitelist()
	def get_student_details(self):
		data={}
		for allotment in frappe.get_all("Hostel Allotment",{"student":self.student,"docstatus":1},["building", "to_room","room_type", "floor","hostel_admission", "available_beds"],limit=1):
			data.update(allotment)
		return data

	def validate_duplicate(self):
		for d in frappe.get_all("Hostel Deallotment",{"docstatus":1,"building":self.building,"room_type":self.room_type,"floor":self.floor,"room":self.room, 'hostel_admission':self.hostel_admission}):
			frappe.throw("Record is Exist <b>{0}</b>".format(d.name))


	def on_submit(self):
		self.create_allotment_ledger(self.room,1)
		self.update_hostel_admision_status()
		self.validate_fees()
		self.update_hostel_allotment()

	def update_hostel_admision_status(self):
		admission=frappe.get_doc("Hostel Admission",self.hostel_admission)
		admission.status="Left"
		admission.submit()

	def validate_fees(self):
		if self.hostel_admission:
			for fees in frappe.get_all("Fees",{"hostel_admission":self.hostel_admission,"outstanding_amount":("!=",0)},["name"]):
				frappe.throw("Your Fee is Not Paid <b>{0}</b>".format(fees.name))

	def on_cancel(self):
		for entries in frappe.get_all("Allotment  Ledger",{"reference_doctype":self.doctype,"reference_name":self.name}):
			frappe.delete_doc("Allotment  Ledger",entries.name)

	def create_allotment_ledger(self,room,bed):
		allotment_ledger=frappe.new_doc("Allotment  Ledger")
		allotment_ledger.student=self.student
		allotment_ledger.hostel_room=room
		allotment_ledger.allotment_date=self.date
		allotment_ledger.no_of_beds=bed
		allotment_ledger.reference_doctype = self.doctype
		allotment_ledger.reference_name = self.name
		allotment_ledger.allotment_type="Add Balance"
		allotment_ledger.save()
		# self.update_hostel_room(room,bed)

	def update_hostel_allotment(self):
		for d in frappe.get_all("Hostel Allotment",{"student":self.student,"to_room":self.room,"docstatus":1,"building":self.building},['name'],order_by="modified desc",limit=1):
			allotment=frappe.get_doc("Hostel Allotment",d.name)
			allotment.deallotment_date=today()
			allotment.submit()

@frappe.whitelist()
def get_allotment_students(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT student,student_name from `tabHostel Allotment` Where (student like '%{0}%' or student_name like '%{0}%') GROUP BY student""".format(txt))