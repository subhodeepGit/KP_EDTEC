import frappe
from kp_edtec.ed_tec.validations.reevalution_application import validate_exam_declaration,validate_post_exam_declaration, validate_course
from kp_edtec.ed_tec.utils import duplicate_row_validation

def validate(doc, method):
	validate_exam_declaration(doc)
	validate_post_exam_declaration(doc)
	validate_course(doc)
	duplicate_row_validation(doc,'photocopy_item',['course','course_name'])


