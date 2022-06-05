import frappe
from kp_edtec.ed_tec.doctype.user_permission import add_user_permission

# bench execute ed_tec.patches.course_patch.add_user_permission_to_course
def add_user_permission_to_course():
    for cr_enroll in frappe.get_all("Course Enrollment",["program_enrollment","student","course","name"]):
        print(cr_enroll.name)
        student=frappe.get_doc("Student",cr_enroll.student)
        if student.student_email_id:
            add_user_permission("Course",cr_enroll.course, student.student_email_id,dict(doctype="Course Enrollment",name=cr_enroll.name))