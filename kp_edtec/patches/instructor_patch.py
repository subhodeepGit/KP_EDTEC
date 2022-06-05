import frappe

# ed_tec.patches.instructor_patch.update_instructor_permissions
def execute():
    delete_user_permission()
    update_instructor_log()
    update_instructor_permissions()
    
def update_instructor_permissions():
    for d in frappe.get_all("Instructor"):
        doc=frappe.get_doc("Instructor",d.name)
        doc.save()

def delete_user_permission():
    for d in frappe.get_all("User Permission",{"reference_doctype":"Instructor"}):
        frappe.delete_doc("User Permission",d.name)

def update_instructor_log():
    for d in frappe.get_all("Instructor"):
        doc=frappe.get_doc("Instructor",d.name)
        for log in doc.get("instructor_log"):
            log.course_name=frappe.db.get_value("Course",log.course,'course_name')
            log.course_code=frappe.db.get_value("Course",log.course,'course_code')
        doc.save()