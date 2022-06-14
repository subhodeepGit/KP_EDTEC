import frappe
from kp_edtec.kp_edtec.validations.course import validate_semester

def validate(doc, method):
	validate_semester(doc)


