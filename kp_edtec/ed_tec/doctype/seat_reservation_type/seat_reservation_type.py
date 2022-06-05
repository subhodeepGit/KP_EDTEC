# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SeatReservationType(Document):
	pass


@frappe.whitelist()
def get_docs(pdoctype, txt, searchfield, start, page_len, filters):
	return frappe.get_all("Seat Reservation based on" , { 'parent': "Educations Configurations"}, ['category'],as_list = 1)