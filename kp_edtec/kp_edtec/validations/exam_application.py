import frappe
from frappe import utils

def validate(doc, method):
	validate_program_academic_year(doc)
	validate_exam_declaration (doc)

def validate_program_academic_year(doc):
	if doc.academic_term not in [d.name for d in frappe.get_all("Academic Term", {'academic_year':doc.get('program_academic_year')},['name'])]:
		frappe.throw("Academic Term <b>'{0}'</b> not belongs to program academic year <b>'{1}'</b>".format(doc.get('academic_term'), doc.get('program_academic_year')))

def validate_exam_declaration (doc):
	if len(frappe.get_all("Program Enrollment",{"student":doc.get('student'),"docstatus":1},['programs',"program"]))!=0:
		for d in frappe.get_all("Program Enrollment",{"student":doc.get('student'),"docstatus":1},['programs',"program"]):
			exam_declaration_list  = [d.name for d in frappe.get_all("Exam Declaration",{"exam_program":d.get("programs"),"docstatus":1, "disabled":0},["name","exam_name"])]
			if exam_declaration_list:
				if doc.exam_declaration not in exam_declaration_list:
					frappe.throw("Exam declaration <b>'{0}'</b> not belongs to programs of student <b>'{1}'</b> or today's date not between application start date and end date.".format(doc.get('exam_declaration'), doc.get('student')))
