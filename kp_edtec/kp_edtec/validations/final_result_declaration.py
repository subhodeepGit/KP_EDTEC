from kp_edtec.kp_edtec.utils import academic_term, semester_belongs_to_programs

def validate(doc, method):
	academic_term(doc)
	semester_belongs_to_programs(doc)