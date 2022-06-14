import frappe
# bench execute kp_edtec.patches.student_group_patch.execute
def execute():
    set_course_name()

def set_course_name():
    for sg in frappe.get_all("Student Group"):
        print(sg.name)
        doc=frappe.get_doc("Student Group",sg.name)
        for cr in doc.get("instructors"):
            for course in frappe.get_all("Course",{"name":cr.course},["course_name"]):
                frappe.db.set_value(cr.doctype,cr.name,'course_name',course.course_name)