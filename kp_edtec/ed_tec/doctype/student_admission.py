import frappe
from kp_edtec.ed_tec.utils import semester_belongs_to_programs,academic_term
def validate(doc,method):
    academic_term(doc)
    validate_total_seats(doc)
    validate_parameters(doc)
    semester_belongs_to_programs(doc)


@frappe.whitelist()
def get_sem(pdoctype, txt, searchfield, start, page_len, filters):
    fltr={"parent":filters.get("program")}
    lst = []
    if txt:
        fltr.update({"semesters":['like', '%{}%'.format(txt)]})
    for i in frappe.get_all("Semesters",fltr,['semesters']):
        if i.semesters not in lst:
            lst.append(i.semesters)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_doc(pdoctype, txt, searchfield, start, page_len, filters):
    doc_list = ['Program Grades', 'Programs', 'Program', 'Student Category', 'Academic Year','Academic Term', 'Student Admission', 'Counselling Structure', 'Bank', 'Bank Account Type', 'Student Applicant']
    return frappe.get_all("DocType" , {"name":["in", doc_list]}, ['name'],as_list = 1)

def validate_total_seats(doc):
    if doc.total_seats==0:
        frappe.throw("Please fill the <b>Total Seats</b> & Set <b>Reservations Distribution</b>")

def validate_parameters(doc):
    for d in doc.get("eligibility_parameter_list"):
        if d.total_score==0:
            frappe.throw("#Row {0} Please Give The <b>Total Score</b> More than Zero".format(d.idx))


@frappe.whitelist()
def get_counselling_structure(pdoctype, txt, searchfield, start, page_len, filters):
    fltr={}
    if filters.get("program_grade") and filters.get("programs") and filters.get("academic_year"):
        dept = frappe.db.get_value("Programs",filters.get("programs"),'department')
        fltr.update({
            "program_grade":filters.get("program_grade"),
            "department":frappe.db.get_value("Department",{'name':dept}, 'parent_department'),
            "academic_year":filters.get("academic_year"),
            'name': ['like', '%{}%'.format(txt)]
        })
        return frappe.get_all("Counselling Structure",fltr,['name'],as_list = 1)
    else:
        frappe.msgprint("Please Select <b>Program Grade</b> , <b>Admission Program</b> and <b>Academic Year</b>  first")
        return []


