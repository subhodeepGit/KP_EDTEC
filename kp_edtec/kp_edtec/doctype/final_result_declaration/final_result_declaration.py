# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from pytz import all_timezones, country_names
import frappe
from frappe.model.document import Document
from frappe.utils.data import nowtime
from frappe.utils.background_jobs import enqueue
from frappe.utils import cint, flt, cstr
from frappe import _
from kp_edtec.kp_edtec.utils import duplicate_row_validation

class FinalResultDeclaration(Document):
	def validate(self):
		validate_semester(self)
		duplicate_row_validation(self,'result_declaration_student',['student'])
	
	@frappe.whitelist()
	def make_exam_assessment_result(self):
		self.db_set("result_creation_status", "In Process")
		frappe.publish_realtime("final_result_declaration_progress",
			{"progress": "0", "reload": 1}, user=frappe.session.user)

		total_records = len(self.get("result_declaration_student"))
		if total_records > 10:
			frappe.msgprint(_('''Fee records will be created in the background.
				In case of any error the error message will be updated in the Schedule.'''))
			enqueue(create_exam_assessment_result, queue='default', timeout=6000, event='create_exam_assessment_result',
				final_result_declaration=self.name)

		else:
			create_exam_assessment_result(self.name)

@frappe.whitelist()
def validate_semester(doc):
	if doc.semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('programs')},['semesters'])]:
		frappe.throw("Semester <b>'{0}'</b> not belongs to programs <b>'{1}'</b>".format(doc.get('semester'), doc.get('programs')))

def create_exam_assessment_result(final_result_declaration):
	doc = frappe.get_doc("Final Result Declaration", final_result_declaration)
	error = False
	total_records = len(doc.get("result_declaration_student"))
	created_records = 0
	if not total_records:
		frappe.throw(_("Please setup Students under Student Groups"))

	for d in doc.get("result_declaration_student"):
		if d.completion_status=="Pending":
			frappe.throw("#Row {0} Completion Status Should be <b>Completed</b>".format(d.idx))

	for d in doc.get("result_declaration_student"):
		# try:
		result=frappe.new_doc("Exam Assessment Result")
		result.student=d.student
		result.grading_scale=doc.grading_scale

		for enroll in frappe.get_all("Program Enrollment",{'student':d.student,'docstatus':1,"academic_year":doc.academic_year},['programs', 'program', 'academic_year', 'academic_term'],limit=1):
			result.programs=enroll.programs
			result.program=enroll.program
			result.academic_year=enroll.academic_year
			result.academic_term=enroll.academic_term

		for allocation in frappe.get_all("Assessment Credits Allocation",{"docstatus":1,"student":d.student,"academic_year":doc.academic_year},["course","earned_credits","total_credits","final_marks","out_of_marks","assessment_criteria"]):
			result.append("assessment_result_item",{
				"course":allocation.course,
				"earned_cr":allocation.earned_credits,
				"total_cr":allocation.total_credits,
				"earned_marks":allocation.final_marks,
				"total_marks":allocation.out_of_marks,
				"assessment_criteria":allocation.assessment_criteria
			})
		
		course_list={}
		duplicate=[]
		for assessment_item in result.get("assessment_result_item"):
			earned_cr=earned_marks=total_cr=total_marks=0
			if assessment_item.course not in duplicate:
				for d in result.get("assessment_result_item"):
					if assessment_item.course==d.course:
						earned_cr+=d.earned_cr
						earned_marks+=d.earned_marks
						total_cr+=d.total_cr
						total_marks+=d.total_marks
				course_list[assessment_item.course]={"earned_cr":earned_cr,"earned_marks":earned_marks,"total_cr":total_cr,"total_marks":total_marks}	
				duplicate.append(assessment_item.course)
				
				

		# for d in course_list:
		# 	result.append("course_final_result",{
		# 		"course":d,
		# 		"earned_cr":course_list[d]['earned_cr'],
		# 		"total_cr":course_list[d]['total_cr'],
		# 		"earned_marks":course_list[d]['earned_marks'],
		# 		"total_marks":course_list[d]['total_marks']
		# 	})
		result.save()
		created_records += 1
		frappe.publish_realtime("final_result_declaration_progress", {"progress": str(int(created_records * 100/total_records)),"current":str(created_records),"total":str(total_records)}, user=frappe.session.user)

		# except Exception as e:
		# 	error = True
		# 	err_msg = frappe.local.message_log and "\n\n".join(frappe.local.message_log) or cstr(e)

	# if error:
	# 	frappe.db.rollback()
	# 	frappe.db.set_value("Final Result Declaration", final_result_declaration, "result_creation_status", "Failed")
	# 	frappe.db.set_value("Final Result Declaration", final_result_declaration, "error_log", err_msg)

	# else:
	# 	frappe.db.set_value("Final Result Declaration", final_result_declaration, "result_creation_statuss", "Successful")
	# 	frappe.db.set_value("Final Result Declaration", final_result_declaration, "error_log", None)
	frappe.db.set_value("Final Result Declaration", final_result_declaration, "result_creation_status", "Successful")
	frappe.publish_realtime("final_result_declaration_progress",
		{"progress": "100", "reload": 1}, user=frappe.session.user)

@frappe.whitelist()
def get_enroll_students(programs=None,semester=None,academic_year=None,academic_term=None):
	if not academic_year:
		frappe.throw("Select Academic Year")
	if not academic_term:
		frappe.throw("Select Academic Term")
	filter={}
	if programs:
		filter.update({"programs":programs})
	if semester:
		filter.update({"semesters":semester})
	if academic_year:
		filter.update({"academic_year":academic_year})
	if academic_term:
		filter.update({"academic_term":academic_term})
	students=[]
	for student in frappe.get_all("Current Educational Details",filter,['parent'],group_by="parent"):
		completed=False
		for course_enroll in frappe.get_all("Course Enrollment",{"student":student.parent,"academic_year":academic_year}):
			for enroll_item in frappe.get_all("Credit distribution List",{"parent":course_enroll.name},['assessment_criteria']):
				completed=True
				if len(frappe.get_all("Assessment Credits Allocation",{'student':student.parent,'assessment_criteria':enroll_item.assessment_criteria,"academic_year":academic_year,"docstatus":1}))==0:
					completed=False				
		for d in frappe.get_all("Student",{"name":student.parent},["name","title"]):
			d.update({"completion_status":"Pending"})
			if completed:
				d.update({"completion_status":"Completed"})
			students.append(d)
	if len(students)==0:
		frappe.msgprint("No Records Found")
	return students

