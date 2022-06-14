import frappe
from frappe import utils
from kp_edtec.kp_edtec.validations.student_admission import validate_academic_year
from kp_edtec.kp_edtec.validations.course import validate_semester
from erpnext.education.doctype.student_group.student_group import get_program_enrollment
from kp_edtec.kp_edtec.utils import get_courses_by_semester

def validate(doc, method):
    validate_academic_year(doc)
    validate_semester(doc)
    validate_course(doc)
    # validate_students(doc)

def validate_students(doc):
    for i in doc.students:
        if i.student:
            if doc.group_based_on != "Activity":
                enrolled_students = get_program_enrollment(doc.academic_year, doc.academic_term,
                doc.program, doc.batch, doc.student_category)
                student_group_student = frappe.db.sql_list('''select student from `tabStudent Group Student` where parent=%s''',
                    (doc.name))
                students = ([d.student for d in enrolled_students if d.student not in student_group_student]
                    if enrolled_students else [""]) or [""]
                # {"program":["IN",program]}
                stud =frappe.db.get_all('Student',{"name":["IN",students]},['name'] )
                print("#### stud",stud)
        # else:
        #   return frappe.db.sql("""select name, title from tabStudent
        #       where `{0}` LIKE %s or title LIKE %s
        #       order by idx desc, name
        #       limit %s, %s""".format(searchfield),
        #       tuple(["%%%s%%" % txt, "%%%s%%" % txt, start, page_len]))

            if i.student not in [d.name for d in stud]:
                frappe.throw("Student <b>'{0}'</b> is not valid".format(i.student ))
#   
# if filters.get("group_based_on") != "Activity":
#       enrolled_students = get_program_enrollment(filters.get('academic_year'), filters.get('academic_term'),
#           filters.get('program'), filters.get('batch'), filters.get('student_category'))
#       student_group_student = frappe.db.sql_list('''select student from `tabStudent Group Student` where parent=%s''',
#           (filters.get('student_group')))
#       students = ([d.student for d in enrolled_students if d.student not in student_group_student]
#           if enrolled_students else [""]) or [""]
#       return frappe.db.sql("""select name, title from tabStudent
#           where name in ({0}) and (`{1}` LIKE %s or title LIKE %s)
#           order by idx desc, name
#           limit %s, %s""".format(", ".join(['%s']*len(students)), searchfield),
#           tuple(students + ["%%%s%%" % txt, "%%%s%%" % txt, start, page_len]))
#   else:
#       return frappe.db.sql("""select name, title from tabStudent
#           where `{0}` LIKE %s or title LIKE %s
#           order by idx desc, name
#           limit %s, %s""".format(searchfield),
#           tuple(["%%%s%%" % txt, "%%%s%%" % txt, start, page_len]))   

def validate_course(doc):
    if doc.course:
        if doc.exam_declaration:
            if doc.course not in [d.courses for d in frappe.get_all("Exam Courses",{"parent":doc.exam_declaration},['courses'])]:
                frappe.throw("Course <b>'{0}'</b> not belongs to exam declaration <b>'{1}'</b>".format(doc.course, doc.exam_declaration))

        if doc.group_based_on=="Combined Course":
            semesters=[sem.name for sem in frappe.get_all("Program",{"programs":["IN",[d.programs for d in doc.get("multiples_programs")]]})]
            if doc.course not in get_courses_by_semester(semesters):
                frappe.throw("Course <b>'{0}'</b> not belongs to Programs <b>'{1}'</b>".format(doc.course, [d.programs for d in doc.get("multiples_programs")]))
        elif doc.course not in get_courses_by_semester(doc.program):
            frappe.throw("Course <b>'{0}'</b> not belongs to semester <b>'{1}'</b>".format(doc.course, doc.program))


