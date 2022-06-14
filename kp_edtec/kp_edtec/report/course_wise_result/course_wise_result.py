# Copyright (c) 2013, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from erpnext.education.api import get_grade

def execute(filters=None):
	columns=get_columns()
	data=get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname":"student",
			"label":"Student",
			"fieldtype":"Link",
			"options":"Student"
		},
		{
			"fieldname":"student_name",
			"label":"Student Name",
			"fieldtype":"Data"
		},
		{
			"fieldname":"academic_year",
			"label":"Academic Year",
			"fieldtype":"Link",
			"options":"Academic Year"
		},
		{
			"fieldname":"academic_term",
			"label":"Academic Term",
			"fieldtype":"Link",
			"options":"Academic Term"
		},
		{
			"fieldname":"programs",
			"label":"Programs",
			"fieldtype":"Link",
			"options":"Programs"
		},
		{
			"fieldname":"semester",
			"label":"Semester",
			"fieldtype":"Link",
			"options":"Program"
		},
		{
			"fieldname":"course",
			"label":"Course",
			"fieldtype":"Link",
			"options":"Course"
		},
		{
			"fieldname":"earned_credits",
			"label":"Earned Credits",
			"fieldtype":"Float"
		},
		{
			"fieldname":"total_credits",
			"label":"Total Credits",
			"fieldtype":"Float"
		},
		{
			"fieldname":"earned_marks",
			"label":"Earned Marks",
			"fieldtype":"Float"
		},
		{
			"fieldname":"total_marks",
			"label":"Total Marks",
			"fieldtype":"Float"
		},
		{
			"fieldname":"grade",
			"label":"Grade",
			"fieldtype":"Data"
		},
		{
			"fieldname":"result",
			"label":"Result",
			"fieldtype":"Data"
		},
	]

def get_data(filters):
	data=[]
	condition=""
	for fltr in ["academic_year","academic_term","course"]:
		if filters.get(fltr):
			condition+=" AND {0}='{1}'".format(fltr,filters.get(fltr))

	query=frappe.db.sql("""
			SELECT 
					cr_all.student,
					cr_all.student_name,
					cr_all.roll_no,
					cr_all.academic_year,
					cr_all.academic_term,
					cr_all.course,
					cr.passing_marks,
					SUM(cr_all.earned_credits) as 'earned_credits',
					SUM(cr_all.total_credits) as 'total_credits',
					SUM(cr_all.final_marks) as 'earned_marks',
					SUM(cr_all.out_of_marks) as 'total_marks'
			FROM `tabAssessment Credits Allocation` cr_all 
			LEFT JOIN `tabCourse` cr ON cr.name=cr_all.course
			WHERE cr_all.docstatus=1 {0}
		    GROUP BY cr_all.student;
		""".format(condition),as_dict=1)
		
	for d in query:
		if filters.get("grading_scale"):
			d['grade']=get_grade(filters.get("grading_scale"), (flt(d.earned_marks)/flt(d.total_marks))*100)
		
		if flt(d.passing_marks) > flt(d.earned_marks):
			d['result']="F"
		else:
			d['result']="P"

		fltr_enroll={"student":d.student,"academic_year":d.academic_year,"academic_term":d.academic_term,"course":d.course}
		if filters.get("semester"):
			fltr_enroll["semester"]=filters.get("semester")

		for enroll in frappe.get_all("Course Enrollment",fltr_enroll,['semester']):
			fltr_sem={"name":enroll.semester}
			if filters.get("programs"):
				fltr_sem["programs"]=filters.get("programs")

			for sem in frappe.get_all("Program",fltr_sem,['programs','name']):
				d.update({
					"programs":sem.programs,
					"semester":sem.name
				})
				data.append(d)	
	return data
