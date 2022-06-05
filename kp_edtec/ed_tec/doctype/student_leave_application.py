import frappe
# @frappe.whitelist()
# def get_group(doctype, txt, searchfield, start, page_len, filters):
#     fltr = {}
#     lst = []
#     if txt:
#         fltr.update({"parent":txt})
#     for i in frappe.get_all("Student Group Student",{'student':filters.get("student")},['parent']):
#         if i.parent not in lst:
#                 lst.append(i.parent)
#     return [(d,) for d in lst]

@frappe.whitelist()
def get_group(doctype, txt, searchfield, start, page_len, filters):
    fltr = {'student':filters.get("student")}
    lst = []
    if txt:
        fltr.update({"parent":['like', '%{}%'.format(txt)]})
    for i in frappe.get_all("Student Group Student",fltr,['parent']):
        if i.parent not in lst:
            lst.append(i.parent)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_course_schedule(doctype, txt, searchfield, start, page_len, filters):
    fltr = {'student':filters.get("student")}
    lst = []
    if txt:
        fltr.update({"parent":['like', '%{}%'.format(txt)]})
    for i in frappe.get_all("Student Group Student",fltr,['parent']):
        if i.parent not in lst:
            lst.append(i.parent)
    
    return frappe.get_all("Course Schedule",{"student_group":["IN",lst]},["name"],as_list=1)
    
    
 