import frappe
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions

def validate(doc,method):
    update_user(doc)

def create_permissions(doc,user):
    delete_ref_doctype_permissions(["Programs","Student"],doc)
    for log in doc.get("instructor_log"):
        add_user_permission("Programs",log.programs, user, doc)
        for enroll in frappe.get_all("Program Enrollment",{"programs":log.programs,"program":log.program,"academic_year":log.academic_year,"academic_term":log.academic_term},['student']):
            add_user_permission("Student",enroll.student, user, doc)
    
# def set_instructors_read_only_permissions(doc):
#     for instr in frappe.get_all("Instructor", {'name':("!=",doc.name)}, ['name','employee']):
        
#         # new instructor permission to old records
#         for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id']): 
#             if emp.user_id:
#                 docshare_permission(emp.user_id,doc.name)

#         # old instructor permissions to new records
#         for cur_emp in frappe.get_all("Employee",{"name":doc.employee},['user_id']):
#             docshare_permission(cur_emp.user_id,instr.name)

def on_trash(doc,method):
    if doc.employee:
        user_id=frappe.db.get_value("Employee",doc.employee,'user_id')
        if user_id:
            user=frappe.get_doc("User",user_id)
            user.module_profile=""
            user.save()


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_instructor_by_student_group(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Student Group Instructor",{"parent":filters.get("student_group"),"instructor": ["like", "%{0}%".format(txt)]},['instructor'],as_list=1)

def update_user(doc):
    if doc.employee:
        user_id=frappe.db.get_value("Employee",doc.employee,'user_id')
        if user_id:
            user=frappe.get_doc("User",user_id)
            user.module_profile="Instructor"
            user.role_profile_name="Employee Role"
            user.save()

            for ur_pr in frappe.get_all("User Permission",{'user':user_id,'allow':"Employee",'for_value':doc.employee,"applicable_for":("!=","Employee")}):
                user_permission=frappe.get_doc("User Permission",ur_pr.name)
                user_permission.applicable_for="Employee"
                user_permission.apply_to_all_doctypes=0
                user_permission.applicable_for="Employee"
                user_permission.reference_doctype=doc.doctype
                user_permission.reference_docname=doc.name
                if len(frappe.get_all("User Permission",{'user':user_id,'allow':"Employee",'for_value':doc.employee,"applicable_for":"Employee"}))==0:
                    user_permission.save()

            # create_permissions(doc,user_id)
    # set_instructors_read_only_permissions(doc)

# def docshare_permission(user,docname):
#     docshare = frappe.new_doc('DocShare')
#     docshare.user = user
#     docshare.share_doctype = "Instructor"
#     docshare.share_name = docname
#     docshare.read = 1
#     docshare.insert()
