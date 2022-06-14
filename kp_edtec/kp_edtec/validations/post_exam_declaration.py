import frappe

def validate(doc, method):
	validate_fee_structure(doc)

def validate_fee_structure(doc):
	exam_program_list = frappe.db.get_value("Exam Declaration",{"name":doc.get("exam_declaration"),"docstatus":1},['exam_program'])
	for f in doc.fee_structure:
		if f.fee_structure:
			if f.fee_structure not in [p['name'] for p in frappe.get_all("Fee Structure",{"programs":["in",exam_program_list],"fee_type":"Post Exam","docstatus":1},['name'])]:
				frappe.throw("Fee structure <b>'{0}'</b> not belongs to exam declaration<b>'{1}'</b> ".format(f.fee_structure,doc.get("exam_declaration")))
