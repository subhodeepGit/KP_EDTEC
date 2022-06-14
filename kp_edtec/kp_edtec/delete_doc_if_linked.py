import frappe
from frappe import _

BENCH_PATH = frappe.utils.get_bench_path()

def execute():
	update_raise_link_exists_exception_msg()
def update_raise_link_exists_exception_msg():
	file_path = "{}/{}".format(BENCH_PATH,
							   "apps/frappe/frappe/model/delete_doc.py")
	with open(file_path) as f:
		if 'raise_link_exists_exception = custom_raise_link_exists_exception' in f.read():
			return
	with open(file_path, "a+") as f:
		f.write(
			"\nfrom kp_edtec.kp_edtec.delete_doc_if_linked import custom_raise_link_exists_exception")
		f.write(
			"\nraise_link_exists_exception = custom_raise_link_exists_exception")
		print("frappe/model/delete_doc.py modified to activate workspaceperms.")

def custom_raise_link_exists_exception(doc, reference_doctype, reference_docname, row=''):
	doc_link = '<a href="/app/Form/{0}/{1}">{1}</a>'.format(doc.doctype, doc.name)
	reference_link = '<a href="/app/Form/{0}/{1}">{1}</a>'.format(reference_doctype, reference_docname)

	#hack to display Single doctype only once in message
	if reference_doctype == reference_docname:
		reference_doctype = ''
	translation = get_name_translation(doc.doctype)
	doctype_label = translation.translated_text if translation else doc.doctype
	translation = get_name_translation(reference_doctype)
	ref_doctype_label = translation.translated_text if translation else reference_doctype
	frappe.throw(_('Cannot delete or cancel because {0} {1} is linked with {2} {3} {4}')
		.format(doctype_label, doc_link, ref_doctype_label, reference_link, row), frappe.LinkExistsError)

def get_name_translation(doctype):
	'''Get translation object if exists of current doctype name in the default language'''
	return frappe.get_value('Translation', {
			'source_text': doctype,
			'language': frappe.local.lang or 'en'
		}, ['name', 'translated_text'], as_dict=True)