# Copyright (c) 2022, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from pytz import all_timezones, country_names
from frappe.utils.data import nowtime
from frappe.utils.background_jobs import enqueue
from frappe.utils import cint, flt, cstr
from frappe import _
from kp_edtec.kp_edtec.utils import duplicate_row_validation

class CummulativeMarksheetTool(Document):
	def validate(self):
		pass	
	@frappe.whitelist()
	def make_exam_assessment_result(self):
		self.db_set("result_creation_status", "In Process")
		frappe.publish_realtime("cummulative_marksheet_tool_progress",
			{"progress": "0", "reload": 1}, user=frappe.session.user)

		total_records = len(self.get("cummulative_marksheet_student"))
		if total_records > 10:
			frappe.msgprint(_(''' Records will be created in the background.
				In case of any error the error message will be updated in the Schedule.'''))
			enqueue(create_cummulative_marksheet, queue='default', timeout=6000, event='create_cummulative_marksheet',
				cummulative_marksheet_tool=self.name)

		else:
			create_cummulative_marksheet(self.name)
def create_cummulative_marksheet(cummulative_marksheet_tool):
	print("\n\n\n\n OK")
	print("cummulative_marksheet_tool",cummulative_marksheet_tool)
	doc = frappe.get_doc("Cummulative Marksheet Tool", cummulative_marksheet_tool)
	error = False
	total_records = len(doc.get("cummulative_marksheet_student"))
	created_records = 0
	if not total_records:
		frappe.throw(_("Please setup Students under Student Groups"))

	# for d in doc.get("cummulative_marksheet_student"):
	# 	if d.completion_status=="Pending":
	# 		frappe.throw("#Row {0} Completion Status Should be <b>Completed</b>".format(d.idx))

	for d in doc.get("cummulative_marksheet_student"):
		# try:
		result=frappe.new_doc("Cummulative Marksheet")
		result.student=d.student
		result.student_name=d.student_name
		result.roll_no=d.roll_no
		result.registration_number=d.registration_number

		# for enroll in frappe.get_all("Program Enrollment",{"student":d.student,"docstatus":1,"academic_term":doc.academic_term},['name','academic_year'],order_by="creation asc",limit=1):
		# 	result.year_of_admission=enroll.academic_year
		for enroll in frappe.get_all("Program Enrollment",{"student":d.student,"docstatus":1,"academic_term":doc.academic_term},['programs','academic_term','academic_year'],order_by="creation desc",limit=1):
			result.programs=enroll.programs
			result.academic_term=enroll.academic_term
			result.year_of_completion=enroll.academic_year
		result.year_of_admission=doc.year_of_admission
		semesters=[]	
		for results in frappe.get_all("Exam Assessment Result",{"student":d.student,"docstatus":1},['name','programs','program'],order_by="program asc"):
			for course in frappe.get_all("Evaluation Result Item",{"parent":results.name},['course','earned_cr','grade','course_code','course_name'],order_by="creation asc"):
				# order_by="course_code asc"
				result.append("cummulative_courses_item",{
					"programs":results.programs,
					"semester":results.program,
					"course":course.course,
					"course_code":course.course_code,
					"course_name":course.course_name,
					"cr":course.earned_cr,
					"gr":course.grade
				})
			semesters.append(results.program)
		total_sgpa=0
		for sem in frappe.get_all("Program",{"name":["IN",semesters]},['name',"semester_order"],order_by="semester_order"):
			for results in frappe.get_all("Exam Assessment Result",{"student":d.student,"docstatus":1,'program':sem.name},['sgpa','modified','programs']):
				result.append("cumulatice_grades_item",{
					"semester":sem.name,
					"semester_order":sem.semester_order,
					"sgpa":results.sgpa
				})
				d.programs=results.programs
				d.completed_on=results.modified
				total_sgpa+=results.sgpa
		result.department=frappe.db.get_value("Programs",result.programs,'department')
		if len(result.get("cumulatice_grades_item")):
			result.cgpa=(total_sgpa/len(result.get("cumulatice_grades_item")))	 
			# d.department=frappe.db.get_value("Programs",result.programs,'department')
			# if len(d.get("cumulatice_grades_item")):
			# 	d.cgpa=(total_sgpa/len(d.get("cumulatice_grades_item")))
		result.save()
		created_records += 1
	frappe.msgprint("Record Created")
	frappe.publish_realtime("cummulative_marksheet_tool_progress", {"progress": str(int(created_records * 100/total_records)),"current":str(created_records),"total":str(total_records)}, user=frappe.session.user)
	frappe.db.set_value("Cummulative Marksheet Tool", cummulative_marksheet_tool, "result_creation_status", "Successful")
	frappe.publish_realtime("cummulative_marksheet_tool_progress",
	{"progress": "100", "reload": 1}, user=frappe.session.user)

@frappe.whitelist()
def get_students(academic_term=None, programs=None):
    enrolled_students = get_program_enrollment(academic_term,programs)
    if enrolled_students:
        student_list = []
        for s in enrolled_students:
            if frappe.db.get_value("Student", s.student, "enabled"):
                s.update({"active": 1})
            else:
                s.update({"active": 0})
            student_list.append(s)
        return student_list
    else:
        frappe.msgprint("No students found")
        return []
def get_program_enrollment(academic_term,programs=None):
    condition1 = " "
    condition2 = " "
    if programs:
        condition1 += " and pe.programs = %(programs)s"
    
    return frappe.db.sql('''
        select
            pe.student, pe.student_name
        from
            `tabProgram Enrollment` pe {condition2}
        where
            pe.academic_term = %(academic_term)s  {condition1}
        order by
            pe.student_name asc
        '''.format(condition1=condition1, condition2=condition2),
                ({"academic_term": academic_term,"programs": programs}), as_dict=1)

	