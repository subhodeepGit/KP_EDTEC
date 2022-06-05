import frappe
from frappe import _

def after_insert(doc,method):
	if doc.doctype=="Course Schedule":
		st_grp_doc=frappe.get_doc("Student Group",doc.student_group)
		if st_grp_doc.get("students"):
			for st_table in st_grp_doc.get("students"):
				set_permissions({"doctype":doc.get('doctype'),"name":doc.get('name'),"student":st_table.student})

def on_submit(doc,method):
	set_permissions(doc)

def on_trash(doc,method):
	delete_user_permission(doc)

def on_cancel(doc,method):
	delete_user_permission(doc)

def set_permissions(doc):
	if get_mail_id(doc):
		frappe.permissions.add_user_permission(doc.get('doctype'), doc.get('name'), get_mail_id(doc))

def get_mail_id(doc):
	# if doc.doctype=="Program Enrollment":
	student=doc.get('student') if doc.get('student') else doc.get('student_roll_no')
	return frappe.db.get_value("Student",student,'student_email_id')

def delete_user_permission(doc):
	for ur in frappe.get_all("User Permission",{"allow":doc.doctype,"for_value":doc.name}):
		frappe.delete_doc("User Permission",ur.name)



def add_user_permission(doctype, name, user,ref, ignore_permissions=False, applicable_for=None,is_default=0, hide_descendants=0, apply_to_all_doctypes=1):
	'''Add user permission'''
	from frappe.core.doctype.user_permission.user_permission import user_permission_exists

	if not user_permission_exists(user, doctype, name, applicable_for):
		if not frappe.db.exists(doctype, name):
			frappe.throw(_("{0} {1} not found").format(_(doctype), name), frappe.DoesNotExistError)

		frappe.get_doc(dict(
			doctype='User Permission',
			user=user,
			allow=doctype,
			for_value=name,
			is_default=is_default,
			applicable_for=applicable_for,
			hide_descendants=hide_descendants,
			reference_doctype=ref.get("doctype"),
			reference_docname=ref.get("name"),
			apply_to_all_doctypes = apply_to_all_doctypes
		)).insert(ignore_permissions=ignore_permissions)


def delete_ref_doctype_permissions(document_list,doc):
	for d in document_list:
		for usr in frappe.get_all("User Permission",{"allow":d,"reference_doctype":doc.doctype,"reference_docname":doc.name}):
			frappe.delete_doc("User Permission",usr.name)
