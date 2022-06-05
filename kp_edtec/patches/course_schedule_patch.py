import frappe

def execute():
    set_course_code_and_course_name()

def set_course_code_and_course_name():
    for cr in frappe.get_all("Course Schedule",['name','course']):
        print(cr)
        course_name=frappe.db.get_value("Course",cr.course,'course_name')
        course_code=frappe.db.get_value("Course",cr.course,'course_code')
        frappe.db.set_value("Course Schedule",cr.name,'course_name',course_name)
        frappe.db.set_value("Course Schedule",cr.name,'course_code',course_code)
