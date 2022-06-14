import frappe
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions

# bench execute kp_edtec.patches.student_patch.execute
def execute():
    set_user_permission()

def set_user_permission():
    for stu in frappe.get_all("Student",['user','name']):
        if stu.user:
            for stu_appl in frappe.get_all("Student Applicant",{"student_email_id":stu.user}):
                add_user_permission("Student Applicant",stu_appl.name, stu.user,dict(reference_doctype="Student",reference_docname=stu.name))

            for stu_appl in frappe.get_all("Student Exchange Applicant",{"student_email_id":stu.user}):
                add_user_permission("Student Exchange Applicant",stu_appl.name, stu.user,dict(reference_doctype="Student",reference_docname=stu.name))
