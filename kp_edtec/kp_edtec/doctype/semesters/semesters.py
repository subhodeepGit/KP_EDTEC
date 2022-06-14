# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Semesters(Document):
	pass

@frappe.whitelist()
def get_courses(semester):
	courses=[d.course for d in frappe.get_all("Program Course",{"parent":semester},["course"])]
	return frappe.get_all("Course",{"name":["IN",courses]},['name','course_name','course_code'])
