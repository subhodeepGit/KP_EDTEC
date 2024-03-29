# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import timedelta
from frappe.utils import get_link_to_form, getdate, date_diff, flt
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday
from erpnext.education.doctype.student_attendance.student_attendance import get_holiday_list
from frappe.model.document import Document

class HostelLeaveApplication(Document):
	def validate(self):
		self.validate_holiday_list()
		self.validate_duplicate()
		self.validate_from_to_dates('from_date', 'to_date')

	def on_submit(self):
		self.update_attendance()

	def on_cancel(self):
		self.cancel_attendance()

	def validate_duplicate(self):
		data = frappe.db.sql("""select name from `tabHostel Leave Application`
			where
				((%(from_date)s > from_date and %(from_date)s < to_date) or
				(%(to_date)s > from_date and %(to_date)s < to_date) or
				(%(from_date)s <= from_date and %(to_date)s >= to_date)) and
				name != %(name)s and student = %(student)s and docstatus < 2
		""", {
			'from_date': self.from_date,
			'to_date': self.to_date,
			'student': self.student,
			'name': self.name
		}, as_dict=1)

		if data:
			link = get_link_to_form('Hostel Leave Application', data[0].name)
			frappe.throw(_('Hostel Leave application {0} already exists against the student {1}')
				.format(link, frappe.bold(self.student)), title=_('Duplicate Entry'))

	def validate_holiday_list(self):
		holiday_list = get_holiday_list()
		self.total_leave_days = get_number_of_leave_days(self.from_date, self.to_date, holiday_list)

	def update_attendance(self):
		holiday_list = get_holiday_list()

		for dt in daterange(getdate(self.from_date), getdate(self.to_date)):
			date = dt.strftime('%Y-%m-%d')

			if is_holiday(holiday_list, date):
				continue

			attendance = frappe.db.exists('Student Attendance', {
				'student': self.student,
				'date': date,
				'docstatus': ('!=', 2)
			})
			
			status = 'Present' if self.mark_as_present else 'Absent'
			if attendance:
				# update existing attendance record
				values = dict()
				values['status'] = status
				values['leave_application'] = self.name
				frappe.db.set_value('Student Attendance', attendance, values)
			else:
				# make a new attendance record
				doc = frappe.new_doc('Student Attendance')
				doc.student = self.student
				doc.student_name = self.student_name
				doc.date = date
				doc.attendance_for="Hosteler"
				doc.hostel_leave_application = self.name
				doc.status = "On Leave"
				doc.building=self.hostel_building
				doc.hostel_room=self.room_no
				doc.insert(ignore_permissions=True, ignore_mandatory=True)
				doc.submit()

	def cancel_attendance(self):
		if self.docstatus == 2:
			attendance = frappe.db.sql("""
				SELECT name
				FROM `tabStudent Attendance`
				WHERE
					student = %s and
					(date between %s and %s) and
					docstatus < 2
			""", (self.student, self.from_date, self.to_date), as_dict=1)

			for name in attendance:
				frappe.db.set_value('Student Attendance', name, 'docstatus', 2)

	@frappe.whitelist()
	def get_hostel_details(self):
		for allotment in frappe.get_all("Hostel Allotment",{"student":self.student,"docstatus":1},["building", "to_room","name"]):
			return allotment

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)+1):
		yield start_date + timedelta(n)

def get_number_of_leave_days(from_date, to_date, holiday_list):
	number_of_days = date_diff(to_date, from_date) + 1

	holidays = frappe.db.sql("""
		SELECT
			COUNT(DISTINCT holiday_date)
		FROM `tabHoliday` h1,`tabHoliday List` h2
		WHERE
			h1.parent = h2.name and
			h1.holiday_date between %s and %s and
			h2.name = %s""", (from_date, to_date, holiday_list))[0][0]

	number_of_days = flt(number_of_days) - flt(holidays)

	return number_of_days

@frappe.whitelist()
def get_hosteler_students(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""SELECT distinct student,student_name from `tabHostel Allotment` where docstatus=1 and (student like '%{0}%' or student_name like '%{0}%')""".format(txt))

