# # Copyright (c) 2022, suraj varade and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt,json
from kp_edtec.ed_tec.utils import get_courses_by_semester


class ContinuousEvaluationTool(Document):
	def get_course_details(self):
		course=frappe.get_doc("Course",self.course)
		for d in course.get("credit_distribution"):
			if self.assessment_criteria == d.assessment_criteria:
				return d

	@frappe.whitelist()
	def get_student_allocations(self):

		data_list=[]
		course_details=get_course_details(self)
		for student in frappe.get_all("Course Assessment",{"course":self.course,"assessment_criteria":self.assessment_criteria, "docstatus":1},["student","student_name","roll_no","registration_number"],order_by="roll_no asc",group_by="student"):
			total_earned_marks=total_total_marks=weightage_marks=0
			evaluation=[]
			for d in frappe.get_all("Course Assessment",{"student":student.student,"course":self.course,"assessment_criteria":self.assessment_criteria, "docstatus":1},["name","earned_marks","total_marks",]):
				total_earned_marks+=flt(d.earned_marks)
				total_total_marks+=flt(d.total_marks)
				for cr in frappe.get_all("Credit distribution List",{"parent":self.course,"assessment_criteria":self.assessment_criteria},['total_marks']):
					weightage_marks=total_earned_marks
					# dre
					# weightage_marks=flt((total_earned_marks/total_total_marks)*flt(cr.total_marks))
				d.update({"total_earned_marks":total_earned_marks,"total_total_marks":total_total_marks,"weightage_marks":weightage_marks})
				evaluation.append(d)
			student['rows']=evaluation
			student["weightage_marks"]=weightage_marks
			student["out_of_marks"]=course_details.total_marks or 0
			student["total_credits"]=course_details.credits or 0
			data_list.append(student)

		return data_list
		
@frappe.whitelist()
def make_continuous_evaluation(continuous_evaluation):
	result=json.loads(continuous_evaluation)
	student_data=get_student_allocations_dict(frappe._dict({"course":result.get("course"),"assessment_criteria":result.get("criteria")}))
	if not student_data:
		frappe.msgprint("Students are not available for given details")
	else:
		records=False
		for d in result.get('rows'):
			exist_record = [a.get('name') for a in frappe.db.get_list("Assessment Credits Allocation",{"docstatus":("!=",2),"student":result.get('rows')[d].get("student"),"academic_year":result.get("academic_year"),"academic_term":result.get("academic_term"),'course':result.get("course"),"assessment_criteria":result.get("criteria")}, 'name')]
			if len(exist_record) > 0:
				frappe.msgprint("Record <b>{0}</b> is already exist for student <b>{1}</b>.".format(', '.join(map(str, exist_record)),result.get('rows')[d].get("student")))
			elif result.get('rows')[d].get("final_marks") and result.get('rows')[d].get("earned_credits") :
				doc=frappe.new_doc("Assessment Credits Allocation")
				doc.student=result.get('rows')[d].get("student")
				doc.student_name=result.get('rows')[d].get("student_name")
				doc.roll_no=result.get('rows')[d].get("roll_no")
				doc.registration_number=result.get('rows')[d].get("registration_number")
				doc.academic_year=result.get("academic_year")
				doc.academic_term=result.get("academic_term")
				doc.assessment_criteria=result.get("criteria")
				doc.course=result.get("course")
				doc.course_name=result.get("course_name")
				doc.course_code=result.get("course_code")
				for row in student_data.get(result.get('rows')[d].get("student"))['rows']:
					doc.append("final_credit_item",{
						"course_assessment":row.get("name"),
						"earned_marks":flt(row.get("earned_marks")),
						"total_marks":flt(row.get("total_marks"))
					})
				doc.grace_marks=flt(result.get('rows')[d].get("grace_marks"))
				doc.weightage_marks=flt(result.get('rows')[d].get("weightage_marks"))
				doc.final_marks=flt(result.get('rows')[d].get("final_marks"))
				doc.earned_credits=flt(result.get('rows')[d].get("earned_credits"))
				doc.total_credits=flt(result.get('rows')[d].get("total_credits"))
				doc.out_of_marks=flt(result.get('rows')[d].get("out_of_marks"))			
				doc.save()
				doc.submit()
				records=True
			else:
				frappe.msgprint("Please add final marks and earned credits for student <b>{0}</b>".format(result.get('rows')[d].get("student")))
		if records:
			frappe.msgprint("Records Created")

def get_student_allocations_dict(doc):
	data_list={}
	course_details=get_course_details(doc)
	for student in frappe.get_all("Course Assessment",{"course":doc.course,"assessment_criteria":doc.assessment_criteria, "docstatus":1},["student","student_name","roll_no","registration_number"],group_by="student"):
		total_earned_marks=total_total_marks=weightage_marks=0
		evaluation=[]
		for i,d in enumerate(frappe.get_all("Course Assessment",{"student":student.student,"course":doc.course,"assessment_criteria":doc.assessment_criteria, "docstatus":1},["name","earned_marks","total_marks",])):
			total_earned_marks+=flt(d.earned_marks)
			total_total_marks+=flt(d.total_marks)
			for cr in frappe.get_all("Credit distribution List",{"parent":doc.course,"assessment_criteria":doc.assessment_criteria},['total_marks']):
				weightage_marks=flt((total_earned_marks/total_total_marks)*flt(cr.total_marks))
			d.update({"total_earned_marks":total_earned_marks,"total_total_marks":total_total_marks,"weightage_marks":weightage_marks})
			evaluation.append(d)
		student['rows']=evaluation
		student["weightage_marks"]=weightage_marks
		student["out_of_marks"]=course_details.total_marks or 0
		student["total_credits"]=course_details.credits or 0
		data_list[student.student]=student
	return data_list

def get_course_details(doc):
	course=frappe.get_doc("Course",doc.course)
	for d in course.get("credit_distribution"):
		if doc.assessment_criteria == d.assessment_criteria:
			return d
@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    courses=get_courses_by_semester(filters.get("semester"))
    if courses:
        return frappe.db.sql("""select name,course_name,course_code from tabCourse
			where name in ({0}) and (name LIKE %s or course_name LIKE %s or course_code LIKE %s)
			limit %s, %s""".format(", ".join(['%s']*len(courses))),
			tuple(courses + ["%%%s%%" % txt, "%%%s%%" % txt,"%%%s%%" % txt, start, page_len]))
    return []