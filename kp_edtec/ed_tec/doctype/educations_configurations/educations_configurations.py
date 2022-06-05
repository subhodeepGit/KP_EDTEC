# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EducationsConfigurations(Document):
	def validate(self):
		self.naming_validation()

	def naming_validation(self):
		if self.student_registration_naming and "#" not in self.student_registration_naming:
			frappe.throw("Add <b>#</b> at the end of Naming Series for digits")
		if self.student_registration_naming.startswith("format:") and "-" in self.student_registration_naming and "." not in self.student_registration_naming:
			frappe.throw("Add valid Naming Series  separated by <b>. (Dot)</b>")


