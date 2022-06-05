import frappe
from kp_edtec.ed_tec.validations.course import validate_semester

def validate(doc, method):
	validate_semester(doc)


