import frappe
from kp_edtec.ed_tec.doctype.user_permission import add_user_permission

# ed_tec.patches.exam_declaration_patch.update_exam_declaration_permission
def execute():
    delete_user_permission()
    update_exam_declaration_permission()
    
def update_exam_declaration_permission():
    for ed in frappe.get_all("Exam Declaration",['exam_program','name']):
        for il in frappe.get_all("Instructor Log",{"programs":ed.exam_program},['parent']):
            for i in frappe.get_all("Instructor",{"name":il.parent},['employee']):
                if i.get('employee'):
                    for emp in frappe.get_all("Employee", {'name':i.get('employee')}, ['user_id']):
                        if emp.get('user_id'):
                            add_user_permission("Exam Declaration",ed.name, emp.get('user_id'), dict(doctype="Exam Declaration",name=ed.name),applicable_for="Exam Declaration", apply_to_all_doctypes=0)
                        else:
                            frappe.msgprint("User Id is not created for employee {0} ".format(emp.employee_name))
                else:
                    frappe.msgprint("Instructor {0} is not employee".format(il.parent))

def delete_user_permission():
    for d in frappe.get_all("User Permission",{"reference_doctype":"Exam Declaration"}):
        frappe.delete_doc("User Permission",d.name)
