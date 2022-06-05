# Copyright (c) 2022, suraj varade and contributors
# For license information, please see license.txt

import re
import frappe
from frappe.model.document import Document
from kp_edtec.ed_tec.utils import duplicate_row_validation
from frappe.utils import flt

class CummulativeMarksheet(Document):
	def validate(self):
		self.map_fields()
		self.validate_missing_fields()
		duplicate_row_validation(self,"cumulatice_grades_item",['semester_order'])

	def map_fields(self):
		order_dict={1:"1ST SEM",2:"2ND SEM",3:"3RD SEM",4:"4TH SEM",5:"5TH SEM",6:"6TH SEM",7:"7TH SEM",8:"8TH SEM",9:"9TH SEM",10:"10TH SEM"}
		for d in self.get("cumulatice_grades_item"):
			if not d.semester_order:
				
				db=frappe.db.sql("""select name,semester_order from `tabProgram` where name="%s" """%(d.semester))
				for sem in frappe.db.get_all("Program",{"name":"%s"%(d.semester)},['name',"semester_order"]):
					print("\n\n\n\n")
					print(sem.semester_order)
					print(d.semester)
					print(db)
					d.semester_order=order_dict.get(sem.semester_order)

	def validate_missing_fields(self):
		# pass
		for d in self.get("cumulatice_grades_item"):
			if not d.semester_order:
				frappe.throw("#Row {0} Please select Semester Order <b>OR</b> set Semester Order IN Semester Master".format(d.idx))

	@frappe.whitelist()
	def get_student_details(self):
		for enroll in frappe.get_all("Program Enrollment",{"student":self.student,"docstatus":1},['name','academic_year'],order_by="creation asc",limit=1):
			self.year_of_admission=enroll.academic_year
		for enroll in frappe.get_all("Program Enrollment",{"student":self.student,"docstatus":1},['name','academic_year'],order_by="creation desc",limit=1):
			self.year_of_completion=enroll.academic_year
		
		self.set("cummulative_courses_item",[])
		semesters=[]
		for result in frappe.get_all("Exam Assessment Result",{"student":self.student,"docstatus":1},['name','programs','program'],order_by="program asc"):
			for course in frappe.get_all("Evaluation Result Item",{"parent":result.name},['course','earned_cr','grade','course_code','course_name'],order_by="creation asc"):
				# order_by="course_code asc"
				self.append("cummulative_courses_item",{
					"programs":result.programs,
					"semester":result.program,
					"course":course.course,
					"course_code":course.course_code,
					"course_name":course.course_name,
					"cr":course.earned_cr,
					"gr":course.grade
				})
			semesters.append(result.program)

		total_sgpa=0
		order_dict={1:"1ST SEM",2:"2ND SEM",3:"3RD SEM",4:"4TH SEM",5:"5TH SEM",6:"6TH SEM",7:"7TH SEM",8:"8TH SEM",9:"9TH SEM",10:"10TH SEM"}
		for sem in frappe.get_all("Program",{"name":["IN",semesters]},['name',"semester_order"],order_by="semester_order"):
			for result in frappe.get_all("Exam Assessment Result",{"student":self.student,"docstatus":1,'program':sem.name},['sgpa','programs']):
				# ,'modified'
				self.append("cumulatice_grades_item",{
					"semester":sem.name,
					"semester_order":order_dict.get(sem.semester_order),
					"sgpa":result.sgpa
				})
				self.programs=result.programs
				# self.completed_on=result.modified
				total_sgpa+=result.sgpa
				
		self.department=frappe.db.get_value("Programs",result.programs,'department')
		if len(self.get("cumulatice_grades_item")):
			self.cgpa=(total_sgpa/len(self.get("cumulatice_grades_item")))