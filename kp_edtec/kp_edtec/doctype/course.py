import frappe,json
from frappe import _

def validate(doc,method):
	calculate_total(doc)
	validate_weightage_percentage(doc)

def validate_weightage_percentage(doc):
	total_weightage=0
	for cr in doc.get("credit_distribution"):
		total_weightage+=cr.weightage
	
	if len(doc.get("credit_distribution")) and total_weightage!=100:
		frappe.throw("Total Weightage should be 100%")


@frappe.whitelist()
def get_semesters(doctype, txt, searchfield, start, page_len, filters):
	data = frappe.db.sql("""SELECT semesters from tabSemesters 
		where parent = '{0}'""".format(filters.get("programs")))
	return data 

def validate_credit(doc):
	if doc.total_distribution and doc.maximum_credit:
		if doc.total_distribution > doc.maximum_credit:
			frappe.throw("<b>Total Distribution</b> Must Be Less Than Or Equal To <b>Maximum Credit</b>")

def calculate_total(doc):
	passing_marks=total_credit=passing_credit=weightage_per=0
	for cr in doc.get("credit_distribution"):
		weightage_per+=cr.weightage
		passing_marks+=cr.passing_marks
		total_credit+=cr.credits
		passing_credit+=cr.passing_credits
	# if weightage_per!=100:
	# 	frappe.throw("Please Fill Credit Distribution Below")
	doc.passing_marks=passing_marks
	doc.total_credit=total_credit
	doc.passing_credit=passing_credit


@frappe.whitelist()
def add_course_to_programs(course, programs):
	semesters = json.loads(programs)
	for entry in semesters:
		program = frappe.get_doc('Program', entry)
		program.append('courses', {
			'course': course,
			'course_name': frappe.db.get_value("Course",{'name':course},"course_name"),
		})
		program.flags.ignore_mandatory = True
		program.save()
	frappe.db.commit()
	frappe.msgprint(_('Course {0} has been added to all the selected programs successfully.').format(frappe.bold(course)),
		title=_('Programs updated'), indicator='green')

@frappe.whitelist()
def check_for_semester(course):
	semesters = [p.parent for p in frappe.get_all('Program Course',{'course':course},'parent') ]
	if semesters:
		return semesters

@frappe.whitelist()
def get_semesters_name(course):
	data = []
	for entry in frappe.db.get_all('Program'):
		program = frappe.get_doc('Program', entry.name)
		courses = [c.course for c in program.courses]
		if not courses or course not in courses:
			data.append(program.name)
	return data