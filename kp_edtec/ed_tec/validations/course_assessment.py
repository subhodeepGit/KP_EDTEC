import frappe
from kp_edtec.ed_tec.utils import get_courses_by_semester, academic_term
from frappe.utils import flt

def validate(doc, method):
	validate_exam_declaration(doc)
	academic_term(doc)
	validate_assessment_criteria(doc)
	# validate_student(doc)
	# validate_course_assessment_plan(doc)
	validate_course(doc)
	validate_earned_marks(doc)

def validate_earned_marks(doc):
	if flt(doc.earned_marks) and flt(doc.total_marks) and flt(doc.earned_marks) > flt(doc.total_marks):
		frappe.throw("Earned marks <b>'{0}'</b> should be less than total marks <b>'{1}'</b> ".format(doc.earned_marks, doc.total_marks))


def validate_exam_declaration(doc):
	if doc.student and doc.exam_declaration:
		declarations=[]
		if len(frappe.get_all("Program Enrollment",{"student":doc.student, "docstatus":1},['programs',"program"]))!=0:
			for d in frappe.get_all("Program Enrollment",{"student":doc.student, "docstatus":1},['programs',"program"]):
				filters={"exam_program":d.get("programs"),"docstatus":1}
				for ed in frappe.get_all("Exam Declaration",filters,["name"]):
					if frappe.db.get_value("Examination Semester",{"parent":ed.name,"semester":d.get("program")}):
						declarations.append(ed.name)
				if doc.exam_declaration not in declarations:
					frappe.throw("Exam declaration <b>'{0}'</b> not belongs to student <b>'{1}'</b> ".format(doc.exam_declaration , doc.student))
		
def validate_assessment_criteria(doc):
	if doc.course and doc.assessment_criteria:
		if doc.assessment_criteria not in [j.assessment_criteria for j in frappe.get_all("Credit distribution List",{'parent': doc.course},["assessment_criteria"])]:
			frappe.throw("Assessment criteria <b>'{0}'</b> not belongs to course <b>'{1}'</b> ".format(doc.assessment_criteria,doc.course ))

# def validate_student(doc):
# 	if doc.student not in [d.student for d in frappe.get_all("Student Group Student",{"parent":doc.get("student_group")},["student"])]:
# 		frappe.throw("Student <b>'{0}'</b> not belongs to student group <b>'{1}'</b> ".format(doc.get('student'),doc.get('student_group') ))

def validate_course_assessment_plan(doc):
	if doc.course_assessment_plan not in [d.name for d in frappe.get_all("Course Assessment Plan", {'docstatus': 1,"programs":doc.programs,"program":doc.semester,"academic_year":doc.academic_year},['name'])]:
		frappe.throw("Course assessment plan <b>'{0}'</b> not belongs to program and course".format(doc.get('course_assessment_plan')))

def validate_course(doc):
	if doc.course and doc.semester:
		if doc.course not in  get_courses_by_semester(doc.semester):
			frappe.throw("Course <b>'{0}'</b> not belongs to semester <b>'{1}'</b> ".format(doc.get('course'),doc.get('semester') ))
