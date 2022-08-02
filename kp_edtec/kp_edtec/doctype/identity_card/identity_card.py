# Copyright (c) 2022, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import os
import glob

from marshmallow import pre_dump

class IdentityCard(Document):
	@frappe.whitelist()
	def get_missing_fields(self):
		data={}
		# data["prn"]=frappe.db.get_value("Program Enrollment",{"student":self.student,"docstatus":1},"permanant_registration_number")
		edu_data =frappe.get_all("Current Educational Details",{"parent":self.student},["academic_year", "programs"])
		data["programs"]= edu_data[0]['programs'] if edu_data[0]['programs'] else ""
		data["academic_year"] = edu_data[0]['academic_year'] if edu_data[0]['academic_year'] else ""
		return data

	def validate(self):
		print("\n\n\n\n\n\n")
		print(self.passport_photo)

		roll_name=self.roll_no

		# path=os.chdir('/opt/bench/frappe-bench/sites/erp.soulunileaders.com/public'+self.passport_photo)
		# print("\n\n\n\n\n\n\n")
		# print(os.getcwd())
		# print(list(path))


		# for f in os.listdir():
		# 	# print(f)
		# 	# print(os.path.splitext(f))
		# 	f_name, f_ext = os.path.splitext(f)
		# 	# print(f_name)
		# 	# print(f_ext)
		# 	new_name = ('{}{}'.format(roll_name, f_ext)).strip()
		# 	print(new_name)
		# 	# os.rename(f, new_name)

		# filepath = glob.glob('/opt/bench/frappe-bench/sites/erp.soulunileaders.com/public'+self.passport_photo, recursive=True)
		# print(filepath)
		# for filepath in os.listdir():
		# 	f_ext = os.path.splitext(filepath)
		# 	print(f_ext)

		a=('/opt/bench/frappe-bench/sites/erp.soulunileaders.com/public'+self.passport_photo)
		aa='{}'.format(a)
		print("aa",aa)
		ext=os.path.splitext(a)
		print(ext)
		extstr=ext[1]
		print(extstr)
		b=('/opt/bench/frappe-bench/sites/erp.soulunileaders.com/public/files/'+roll_name+extstr)
		bb='{}'.format(b)
		print(bb)
		os.rename(a, b)
		# new_path="/files/"+roll_name+extstr
		# fr_new_path='{}'.format(new_path)
		# frappe.set_value("Identity Card",self.name,"passport_photo",fr_new_path)