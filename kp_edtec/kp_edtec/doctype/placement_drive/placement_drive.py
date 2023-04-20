# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import msgprint, _
# from kp_edtec.kp_edtec.notification.custom_notification import placement_drive_submit

class PlacementDrive(Document):
	def validate(self):
		validate_application_date(self)

	def on_submit(self):
		# placement_drive_submit(self)
		self.set_permission_to_enroll_student()

	def on_cancel(self):
		self.delete_student_permission()

	def set_permission_to_enroll_student(self):
		for stu in frappe.get_all("Current Educational Details",{"semesters":["IN",[d.semester for d in self.get("for_programs")]],"academic_year":self.academic_year,"academic_term":self.academic_term},['parent'],group_by="parent"):
			docshare = frappe.new_doc('DocShare')
			docshare.user = frappe.db.get_value("Student",stu.parent,'user')
			docshare.share_doctype = self.doctype
			docshare.share_name = self.name
			docshare.read = 1
			docshare.select = 1
			docshare.insert(ignore_permissions=True)

	def delete_student_permission(self):
		for d in frappe.get_all("DocShare",{"share_doctype":self.doctype,"share_name":self.name},['name']):
			frappe.delete_doc("DocShare",d.name)

def validate_application_date(doc):
	if doc.application_start_date and doc.application_end_date:
		if doc.application_end_date < doc.application_start_date:
			frappe.throw(_('Application_end_date <b>{0}</b> should be greater than application_start_date <b>{1}</b>.').format(doc.application_end_date, doc.application_start_date))

