# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HostelAllotment(Document):
	def validate(self):
		self.date_validation()
		self.validate_allocated_room()
		self.validate_to_room()
		self.validate_duplicate()
		self.map_fields_if_shifting()
	
	def validate_to_room(self):
		room_list =[r.name for r in frappe.get_all("Hostel Room",{"building":self.building, "room_type":self.room_type, "floor":self.floor, "disable":0},["name"])]
		if room_list :
			if self.to_room not in room_list:
				self.to_room = 0

	def on_submit(self):
		if self.purpose=="Allotment":
			self.create_allotment_ledger(self.to_room,"Deduct Balance")
		elif self.purpose=="Shifting":
			self.create_allotment_ledger(self.to_room,"Deduct Balance")
			self.create_allotment_ledger(self.from_room,"Add Balance")
		self.update_hostel_admision_status()
	
	def on_cancel(self):
		for entries in frappe.get_all("Allotment  Ledger",{"reference_doctype":self.doctype,"reference_name":self.name}):
			frappe.delete_doc("Allotment  Ledger",entries.name)
		

	def create_allotment_ledger(self,room,allotment_type):
		allotment_ledger=frappe.new_doc("Allotment  Ledger")
		allotment_ledger.student=self.student
		allotment_ledger.hostel_room=room
		allotment_ledger.allotment_date=self.date
		allotment_ledger.no_of_beds=1
		allotment_ledger.allotment_type=allotment_type
		allotment_ledger.hostel_allotment=self.name
		allotment_ledger.reference_doctype = self.doctype
		allotment_ledger.reference_name = self.name
		allotment_ledger.save()
		# self.update_hostel_room(room,bed)

	def update_hostel_room(self,room,bed):
		allocated_beds = frappe.db.sql("""select sum(no_of_beds) as beds from `tabAllotment  Ledger` where hostel_room='{0}'""".format(room), as_dict=1)
		if allocated_beds:
			hostel_room = frappe.get_doc("Hostel Room", room)
			hostel_room.seat_balance = hostel_room.total_capacity - allocated_beds[0]['beds']
			hostel_room.save()
			self.available_beds = hostel_room.seat_balance

	@frappe.whitelist()
	def get_hostel_details(self):
		for hl in frappe.get_all("Hostel Admission",{"student":self.student,"docstatus":1},['name','hostel_type','status'],limit=1):
			self.hostel_admission=hl.name
			self.room_type=hl.hostel_type

			if hl.status=='Allotted':
				self.purpose="Allotment"

			elif hl.status=='Shifted':
				self.purpose="Shifting"
			
	@frappe.whitelist()
	def map_fields_if_shifting(self):
		if self.purpose=="Shifting":
			for d in frappe.get_all("Hostel Allotment",{"docstatus":1,"student":self.student},['allotment_from','allotment_to','building','room_type','from_room','to_room','hostel_admission','floor'],limit=1):
				self.allotment_from=d.allotment_from
				# self.allotment_to=d.allotment_to
				# self.building=d.building
				# self.room_type=d.room_type
				self.hostel_admission=d.hostel_admission
				# self.floor=d.floor
				self.from_room=d.to_room

	def date_validation(self):
		if (self.allotment_from and self.allotment_to) and (self.allotment_from>self.allotment_to):
			frappe.throw("<b>Allotment To</b> Date must be Greater Than <b>Allotment From</b>  Date")
		
	def update_hostel_admision_status(self):
		admission=frappe.get_doc("Hostel Admission",self.hostel_admission)
		if self.purpose=="Allotment":
			admission.status="Allotted"
		elif self.purpose=="Shifting":
			admission.status="Shifted"
		admission.submit()

	def validate_allocated_room(self):
		data = frappe.get_all("Hostel Allotment",{"building":self.building,"to_room":self.to_room,"room_type":self.room_type,"floor":self.floor,"docstatus":1},["name"])
		if data and self.available_beds == 0:
			frappe.throw("The room is already occupied")
		
	def validate_duplicate(self):
		if self.purpose == "Allotment":
			for d in frappe.get_all("Hostel Allotment",{"docstatus":1,"student":self.student,"purpose":"Allotment","allotment_from":['BETWEEN',[self.allotment_from,self.allotment_to]],"allotment_to":['BETWEEN',[self.allotment_from,self.allotment_to]]}):
				frappe.throw("Hostel Allotment Already Exists <b>{0}</b>".format(d.name))

@frappe.whitelist()
def get_hostel_students(doctype, txt, searchfield, start, page_len, filters):
	stud_list1 = frappe.db.sql("""SELECT distinct student,student_name from `tabHostel Admission` where docstatus=1 and (student like '%{0}%' or student_name like '%{0}%')""".format(txt))
	stud_list2 = frappe.db.sql("""SELECT student, student_name from `tabDisciplinary Complaints` 
	where docstatus=1 and complaint_status='Action Taken' and action='Debarred' and (student like '%{0}%' or student_name like '%{0}%')""".format(txt))
	return list(stud_list1) + list(set(stud_list2) - set(stud_list1))

@frappe.whitelist()
def get_rooms(doctype, txt, searchfield, start, page_len, filters):
	return frappe.get_all("Hostel Room",{"building":filters.get("building"), "room_type":filters.get("room_type"), "floor":filters.get("floor"), "disable":0,"seat_balance":(">=",1), "name":('!=',filters.get('from_room'))},["name"],as_list=1)
