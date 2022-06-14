import frappe
from kp_edtec.kp_edtec.utils import get_courses_by_semester,duplicate_row_validation

def validate(doc, method):
    validate_exam_declaration(doc)
    validate_post_exam_declaration(doc)
    validate_course(doc)

def validate_exam_declaration(doc):
    if len(frappe.get_all("Program Enrollment",{"student":doc.get('student'),"docstatus":1},['programs',"program"]))!=0:
        for d in frappe.get_all("Program Enrollment",{"student":doc.get('student'),"docstatus":1},['programs',"program"]):
            if doc.exam_declaration not in [d.name for d in frappe.get_all("Exam Declaration",{"exam_program":d.get("programs"),"docstatus":1},["name"])]:
                frappe.throw("Exam Declaration <b>'{0}'</b> not belongs to program of student <b>'{1}'</b>".format(doc.get('exam_declaration'), doc.get('student')))

def validate_post_exam_declaration(doc):
    if len(frappe.get_all("Program Enrollment",{"student":doc.get('student'),"docstatus":1},['programs',"program"]))!=0:
        for d in frappe.get_all("Program Enrollment",{"student":doc.get('student'),"docstatus":1},['programs',"program"]):
            exam_declaration_list = [d.name for d in frappe.get_all("Exam Declaration",{"exam_program":d.get("programs"),"docstatus":1},["name"])]
            if doc.post_exam_declaration not in [d.name for d in frappe.get_all("Post Exam Declaration",{"exam_declaration":["IN",exam_declaration_list]},["name"])]:
                frappe.throw("Post Exam Declaration<b>'{0}'</b> not belongs to exam declaration <b>'{1}'</b>".format(doc.get('post_exam_declaration'),doc.get('exam_declaration')))

def validate_course(doc):
    program =[]
    if doc.get("post_exam_declaration"):
        for d in frappe.db.get_all("Post Exam Declaration",{"name":doc.get("post_exam_declaration")},["exam_declaration"]):
            program = get_sem_from_exam_declaration(d.get("exam_declaration"), program)
    if doc.get("exam_declaration"):
        program = get_sem_from_exam_declaration(doc.get("exam_declaration"), program)
    for i in doc.photocopy_item:
        if i.course:
            if i.course not in get_courses_by_semester(program):
                frappe.throw("Course <b>'{0}'</b> not belongs to exam declaration <b>'{1}'</b>".format(i.course,doc.get('exam_declaration')))

def get_sem_from_exam_declaration(exam_declaration, program):
    for dcl in frappe.get_all("Exam Declaration",{"name":exam_declaration,"docstatus":1},["name"]):
        for sem in frappe.get_all("Examination Semester",{"parent":dcl.name},["semester"]):
            if sem.semester not in program:
                program.append(sem.semester)
                return program
            else :
                return program