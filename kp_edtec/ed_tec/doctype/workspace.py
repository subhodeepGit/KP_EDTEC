# from ed_tec.ed_tec.doctype.student_admit_card.student_admit_card import StudentAdmitCard
import frappe
from frappe import _, DoesNotExistError, ValidationError, _dict


def create_workspace(role,doctype,):
	if len(frappe.get_all("Workspace",{"name":role}))==0:
		make_doc(role,doctype)
	for wk in frappe.get_all("Workspace",{"name":role}):
		if len(frappe.get_all("Workspace Link",{"link_to":role,"type":"Link"}))==0:
			doc=frappe.get_doc("Workspace",wk.name)
			doc.append("links",{
				"type":"Link",
				"link_type":"DocType",
				"label":doctype,
				"link_type":"DocType",
				"link_to":doctype
				})
			doc.save()


def make_doc(name,doctype):
	doc=frappe.new_doc("Workspace")
	doc.label=name
	doc.cards_label=name
	doc.append("links",{
		"type":"Card Break",
		"link_type":"DocType",
		"label":"Student",
	})
	doc.save()

def make_workspace_for_user(page,user):
	filters = {
		'extends': page,
		'for_user': user
	}
	pages = frappe.get_list("Workspace", filters=filters)
	if pages:
		return frappe.get_doc("Workspace", pages[0])
	doc = frappe.new_doc("Workspace")
	doc.update({
		"module":"ED_TEC",
	})
	doc.for_user = user
	doc.append("links",{
		"type":"Card Break",
		"link_type":"DocType",
		"label":page,
	})
	doc.append("links",{
				"type":"Link",
				"link_type":"DocType",
				"label":"Student Admit Card",
				"link_type":"DocType",
				"link_to":"Student Admit Card"
				})
	doc.label = 'ED_TEC-' + user
	
	doc.insert(ignore_permissions=True)