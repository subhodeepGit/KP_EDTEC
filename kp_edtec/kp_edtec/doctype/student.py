import frappe
from frappe import _
from kp_edtec.kp_edtec.doctype.workspace import make_workspace_for_user
from kp_edtec.kp_edtec.utils import duplicate_row_validation
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from frappe.desk.form.linked_with import get_linked_doctypes

@frappe.whitelist()
def get_student_program(student):
	data=frappe.db.sql("""Select sp.program,sp.academic_term from `tabStudent Applicant` sp 
					left join `tabStudent` s on s.student_applicant=sp.name
					where s.name='{0}' and sp.docstatus=1""".format(student),as_dict=1)

	if len(data)>0:
		return data[0]

def after_insert(doc,method):
	# doc.user=doc.student_email_id
	if doc.student_applicant:
		student_applicant=frappe.get_doc("Student Applicant",doc.student_applicant)
		if student_applicant.get("previous_education_details"):
			for st_app in student_applicant.get("previous_education_details"):
				doc.append("educational_details",{
					"qualification":st_app.qualification,
					"institute":st_app.institute,
					"board":st_app.board,
					"score":st_app.score,
					"percentage":st_app.percentage_cgpa,
					"year_of_completion":st_app.year_of_completion
				})
		doc.append("current_education",{
			"programs":student_applicant.get('programs_'),
			"semesters":student_applicant.get('program'),
			"academic_year":student_applicant.get('academic_year'),
			"academic_term":student_applicant.get('academic_term')
		})

	create_user_permission(doc)
	# make_workspace_for_user(doc.doctype,doc.user)

def on_trash(doc,method):
	if frappe.db.exists("User",doc.user):
		user=frappe.get_doc("User",doc.user)
		user.module_profile=""
		user.save()
	delete_ref_doctype_permissions(["Student"],doc)

def on_update(doc,method):
	if doc.student_applicant:
		frappe.db.set_value("Student Applicant", doc.student_applicant, "application_status", "Approved")

def validate(doc,method):
	update_student_records(doc)
	check_unique(doc)
	duplicate_row_validation(doc, "education_details", ['qualification','percentage'])
	duplicate_row_validation(doc, "siblings", ['full_name', 'gender'])
	duplicate_row_validation(doc, "disable_type", ['disability_type', 'percentage_of_disability'])

def check_unique(doc):
	# make_workspace_for_user("Education",doc.user)
	"""Validates if the Student Exchange Applicant is Unique"""
	if doc.student_exchange_applicant:
		student = frappe.db.sql("select name from `tabStudent` where student_exchange_applicant=%s and name!=%s", (doc.student_exchange_applicant, doc.name))
		if student:
			frappe.throw(_("Student {0} exist against Student Exchange Applicant {1}").format(student[0][0], doc.student_exchange_applicant))

@frappe.whitelist()
def get_sem(doctype, txt, searchfield, start, page_len, filters):
	fltr = {"parent":filters.get("student")}
	if txt:
		fltr.update({"semesters":txt})
	return frappe.get_all("Current Educational Details",fltr,["semesters"],as_list=1)

@frappe.whitelist()
def get_batch(doctype, txt, searchfield, start, page_len, filters):
	fltr = {"student":filters.get("student"),"student_batch_name":("!=","")}
	if txt:
		fltr.update({"student_batch_name":txt})
	return frappe.get_all("Program Enrollment",fltr,["student_batch_name"],as_list=1)


def create_user_permission(doc):
	if doc.user:
		for stu_appl in frappe.get_all("Student Applicant",{"student_email_id":doc.user}):
			add_user_permission("Student Applicant",stu_appl.name, doc.user,doc)

		for stu_appl in frappe.get_all("Student Exchange Applicant",{"student_email_id":doc.user}):
			add_user_permission("Student Exchange Applicant",stu_appl.name, doc.user,doc)

def update_student_records(self):
	linked_doctypes = get_linked_doctypes("Student")
	for d in linked_doctypes:
		meta = frappe.get_meta(d)
		if not meta.issingle:
			if "sams_portal_id" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student":
					frappe.db.sql("""UPDATE `tab{0}` set sams_portal_id = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.sams_portal_id, self.name))
			
			if "permanent_registration_number" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student":
					frappe.db.sql("""UPDATE `tab{0}` set permanent_registration_number = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.permanant_registration_number, self.name))
			
			if "permanant_registration_number" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student":
					frappe.db.sql("""UPDATE `tab{0}` set permanant_registration_number = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.permanant_registration_number, self.name))

			if "registration_number" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student":
					frappe.db.sql("""UPDATE `tab{0}` set registration_number = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.permanant_registration_number, self.name))

			if "roll_no" in [f.fieldname for f in meta.fields]:
				if d != "Student Applicant" and d != "Student" and d != "Student Group":			
					frappe.db.sql("""UPDATE `tab{0}` set roll_no = %s where {1} = %s""".format(d, linked_doctypes[d]["fieldname"][0]),(self.roll_no, self.name))
