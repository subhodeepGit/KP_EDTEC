import frappe
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission

# kp_edtec.patches.exam_paper_setting_patch.update_exam_paper_setting_permission
def execute():
    delete_permission()
    update_exam_paper_setting_permission()

def update_exam_paper_setting_permission():
    for ed in frappe.get_all("Exam Paper Setting",['examiner','moderator_name','name']):
        eps_doc = frappe.get_doc("Exam Paper Setting",ed.name)
        if ed.examiner:
            for i in frappe.get_all("Instructor",{"name":ed.examiner},['employee']):
                if i.get('employee'):
                    for emp in frappe.get_all("Employee", {'name':i.get('employee')}, ['user_id']):
                        if emp.get('user_id'):
                            add_user_permission("Exam Paper Setting",ed.name, emp.get('user_id'), dict(doctype="Exam Paper Setting",name=ed.name),applicable_for="Exam Paper Setting", apply_to_all_doctypes=0)
                else:
                    frappe.msgprint("Instructor {0} is not employee".format(ed.examiner))
        if ed.moderator_name:
            for i in frappe.get_all("Instructor",{"name":ed.moderator_name},['employee']):
                if i.get('employee'):
                    for emp in frappe.get_all("Employee", {'name':i.get('employee')}, ['user_id']):
                        if emp.get('user_id'):
                            add_user_permission("Exam Paper Setting",ed.name, emp.get('user_id'), dict(doctype="Exam Paper Setting",name=ed.name),applicable_for="Exam Paper Setting", apply_to_all_doctypes=0)
                else:
                    frappe.msgprint("Instructor {0} is not employee".format(ed.moderator_name))

def delete_permission():
    for d in frappe.get_all("User Permission",{"reference_doctype":"Exam Paper Setting"}):
        frappe.delete_doc("User Permission",d.name)