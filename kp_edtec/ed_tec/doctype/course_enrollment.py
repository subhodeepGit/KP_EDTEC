import frappe
from kp_edtec.ed_tec.utils import duplicate_row_validation
from kp_edtec.ed_tec.doctype.user_permission import add_user_permission


def validate(doc,method):
	if doc.get("__islocal"):
		create_permission(doc)
		mapping_from_course(doc)
	validate_credit_distribution(doc)
	calculate_credit_distribution(doc)
	mapping_from_program_enrollment(doc)
	duplicate_row_validation(doc, "credit_distribution", ['assessment_criteria',])
	validate_course_enrollment(doc)

def after_insert(doc,method):
	set_permissions(doc)
	set_permission_to_instructor(doc)

def on_trash(doc,method):
	delete_permissions(doc)

def set_permission_to_instructor(doc):
	for p_enroll in frappe.db.get_all("Program Enrollment", {'name':doc.program_enrollment},['programs','program']):
		fltr = {'programs':p_enroll.programs, 'program':p_enroll.program}
		if doc.academic_year:
			fltr.update({'academic_year':doc.academic_year})
		if doc.academic_term:
			fltr.update({'academic_term':doc.academic_term})
		for d in frappe.get_all('Instructor Log',fltr ,'parent'):
			emp = frappe.db.get_value("Instructor", {'name':d.parent}, 'employee')
			docshare = frappe.new_doc('DocShare')
			docshare.user = frappe.db.get_value("Student",{"name":doc.student},"student_email_id")
			docshare.share_doctype = "Instructor"
			docshare.share_name = d.parent
			docshare.read = 1
			docshare.insert(ignore_permissions=True)
	
@frappe.whitelist()
def get_course(doctype, txt, searchfield, start, page_len, filters):
	for pe in frappe.get_all("Program Enrollment",{"name":filters.get("program_enrollment")},["programs"]):
		for pro in frappe.get_all("Programs",{"name":pe.programs},['department']):
			return frappe.get_all("Course",{"department":pro.department},['name','course_code'],as_list=1)
	return []

def create_permission(doc):
	user_id=frappe.db.get_value("Student",{"name":doc.student},"student_email_id")
	if user_id:
		for d in frappe.get_all("Course Schedule",{"course":doc.course}):
			frappe.permissions.add_user_permission("Course Schedule",d.name, user_id)

def mapping_from_course(doc):
	course=frappe.get_doc("Course",doc.course)
	doc.grading_scale=course.default_grading_scale
	doc.total_course_marks=course.total_marks
	doc.total_passing_marks=course.passing_marks
	doc.total_credits=course.total_credit
	doc.passing_credits=course.passing_credit
	for cr in course.get("credit_distribution"):
		doc.append("credit_distribution",{
			"assessment_criteria":cr.assessment_criteria,
			"weightage":cr.weightage,
			"credits":cr.credits,
			"passing_credits":cr.passing_credits,
			"total_marks":cr.total_marks,
			"passing_marks":cr.passing_marks
		})

def validate_credit_distribution(doc):
	for cr in doc.get("credit_distribution"):
		if cr.credits < cr.passing_credits:
			frappe.throw("#Row <b>{0}</b> Credits should be greater than or equal to Passing Credits".format(cr.idx))

		if cr.total_marks < cr.passing_marks:
			frappe.throw("#Row <b>{0}</b> Total Marks should be greater than or equal to Passing Marks".format(cr.idx))


def calculate_credit_distribution(doc):
	passing_marks=total_credit=passing_credit=weightage_per=0
	for cr in doc.get("credit_distribution"):
		weightage_per+=cr.weightage
		passing_marks+=cr.passing_marks
		total_credit+=cr.credits
		passing_credit+=cr.passing_credits
	# if weightage_per!=100:
	#     frappe.throw("Total Weightage Should be 100")
	doc.course_passing_marks=passing_marks
	doc.total_credits=total_credit
	doc.passing_credits=passing_credit

def mapping_from_program_enrollment(doc):
	if not doc.academic_year or not doc.academic_term:
		for enroll in frappe.get_all("Program Enrollment",{"name":doc.program_enrollment},["academic_year","academic_term","program"]):
			doc.academic_year=enroll.academic_year
			doc.academic_term=enroll.academic_term
			doc.program=enroll.program

	for cr in frappe.get_all("Course",{"name":doc.course},['course_name','course_code']):
		doc.course_name=cr.course_name
		doc.course_code=cr.course_code

def set_permissions(doc):
	add_user_permission(doc.doctype,doc.name,frappe.db.get_value("Student",doc.get('student'),'student_email_id'),dict(doctype="Program Enrollment",name=doc.program_enrollment))
	student=frappe.get_doc("Student",doc.student)
	if student.student_email_id:
		add_user_permission("Course",doc.course, student.student_email_id,dict(doctype="Course Enrollment",name=doc.name))

def delete_permissions(doc):
	for usr in frappe.get_all("User Permission",{"allow":doc.doctype,"for_value":doc.name}):
		frappe.delete_doc("User Permission",usr.name)
	for usr in frappe.get_all("User Permission",{"reference_doctype":"Course Enrollment","reference_docname":doc.name}):
		frappe.delete_doc("User Permission",usr.name)  

def validate_course_enrollment(doc):
	filters = {'academic_year':doc.academic_year, "semester":doc.semester, "student":doc.student,"academic_term":doc.academic_term,"name":("!=",doc.name),"course":doc.course}
	existed_enrollment = [p.name for p in frappe.get_all('Course Enrollment', filters, ["name"])]
	if len(existed_enrollment) > 0:
		for e in existed_enrollment:
			if e:
				frappe.throw("Student <b>'{0}'</b> had Course enrollment <b>'{1}'</b> already".format(doc.student,e))