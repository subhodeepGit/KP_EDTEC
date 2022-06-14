import frappe

def validate(doc, method):
    validate_course(doc)
    validate_instructor(doc)
    validate_exam_declaration(doc)
    validate_student_for_student_group(doc)
    validate_instructor_for_course(doc)

def validate_course(doc):
    if not doc.is_exam_schedule and doc.course not in [d.course for d in frappe.get_all("Student Group Instructor",{"parent":doc.get("student_group"),"instructor":doc.get("instructor")},['course'])]:
        frappe.throw("Course <b>'{0}'</b> not belongs to student group <b>'{1}'</b> and instructor <b>'{2}'</b>".format(doc.get('course'), doc.get('student_group'), doc.get('instructor')))

def validate_instructor(doc):
    if not doc.is_exam_schedule and doc.instructor not in [d.instructor for d in frappe.get_all("Student Group Instructor",{"parent":doc.get("student_group")},['instructor'])]:
        frappe.throw("Instructor <b>'{0}'</b> not belongs to student group <b>'{1}'</b> ".format(doc.get('instructor'), doc.get('student_group')))

def validate_exam_declaration(doc):
    ed_list = frappe.db.sql("""SELECT distinct(ed.name) as name from `tabExam Declaration` ed 
    left join `tabExam Courses` c on c.parent=ed.name where c.courses='{0}' and ed.docstatus=1""".format(doc.get("course")), as_dict=1)
    if doc.exam_declaration:
        if doc.exam_declaration not in [d.name for d in ed_list if ed_list]:
            frappe.throw("Exam declaration <b>'{0}'</b> not belongs to course <b>'{1}'</b> ".format(doc.get('exam_declaration'), doc.get('course')))

def validate_student_for_student_group(doc):
    student_list =frappe.db.sql("""SELECT stg.student as student from `tabStudent Group Student` stg 
    left join `tabStudent Group` sg on stg.parent=sg.name where sg.name='{0}' """.format(doc.get("student_group")), as_dict=1)
    for stud in doc.student_paper_code:
        if stud.student not in [s.student for s in student_list]:
            frappe.throw("Student <b>'{0}'</b> not belongs to student group <b>'{1}'</b> ".format(stud.student, doc.get('student_group')))

def validate_instructor_for_course(doc):
    if not doc.is_exam_schedule:
        for i in doc.additional_instructor:
            if i.instructor not in [d.parent for d in frappe.get_all("Instructor Log",{"course":doc.get("course")},['parent'])]:
                frappe.throw("Instructor <b>'{0}'</b> not belongs to course <b>'{1}'</b> ".format(i.instructor, doc.get('course')))
