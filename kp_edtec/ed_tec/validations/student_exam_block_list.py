import frappe

def validate(doc, method):
	validate_semester(doc)
	validate_exam_declaration(doc)
	validate_student(doc)

def validate_exam_declaration(doc):
	if doc.exam_declaration not in [d.name for d in frappe.get_all("Exam Declaration", {"exam_program":doc.get('program'),"docstatus":1},['name'])]:
		frappe.throw("Exam Declaration <b>'{0}'</b> not belongs to program of exam <b>'{1}'</b>".format(doc.get('exam_declaration'), doc.get('program')))

def validate_semester(doc):
	if doc.semester not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('program')},['semesters'])]:
		frappe.throw("Program of exam <b>'{0}'</b> not belongs to semester <b>'{1}'</b>".format(doc.get('program'), doc.get('semester')))

def validate_student(doc):
	student_list =frappe.db.sql("""SELECT distinct(st.name) from `tabStudent` st 
	left join `tabCurrent Educational Details` ced on ced.parent=st.name 
	where ced.programs='{0}'""".format(doc.get("program")), as_dict=1)
	for stud in doc.student_block_item:
		if stud.student not in [s['name'] for s in student_list]:
			frappe.throw("Student <b>'{0}'</b> not belongs to program <b>'{1}'</b> ".format(stud.student, doc.get('program')))

