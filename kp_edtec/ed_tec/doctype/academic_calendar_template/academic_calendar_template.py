# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import date_diff

class AcademicCalendarTemplate(Document):
	def validate(self):
		self.date_validation()
		self.calculate_duration()

	def date_validation(self):
		if len(self.academic_events_table) > 0:
			for aet in self.get("academic_events_table"):
				if aet.end_date and aet.start_date and aet.end_date < aet.start_date:
					frappe.throw("End Date Must Be Greater Than Start Date in Table <b>Academic Events table</b>")

	def calculate_duration(self):
		for events in self.get("academic_events_table"):
			events.duration=(date_diff(events.end_date,events.start_date)+1)