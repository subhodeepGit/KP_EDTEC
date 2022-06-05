# Copyright (c) 2013, suraj varade and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    data = get_data(filters)
    columns = get_columns(filters)
    return columns, data

def get_columns(filters=None):
    return [
    {
        "label": "Student",
        "fieldtype": "Link",
        "fieldname": "student",
        "options":"Student",
        'width':180
    },
    {
        "label": "Student Name",
        "fieldtype": "Data",
        "fieldname": "student_name",
        'width':150
    },
    {
        "label": "Academic Year",
        "fieldtype": "Link",
        "fieldname": "academic_year",
        "options":"Academic Year",
        'width':110
    },
    {
        "label": "Academic Term",
        "fieldtype": "Link",
        "fieldname": "academic_term",
        "options":"Academic Term",
        'width':150
    },
    {
        "label": "Programs",
        "fieldtype": "Link",
        "options":"Programs",
        "fieldname": "programs",
        'width':150
    },
    {
        "label": "Semester",
        "fieldtype": "Link",
        "options":"Program",
        "fieldname": "semester",
        'width':150
    },
    {
        "label":"Course",
        "fieldname":"course",
        "fieldtype":"Link",
        "options":"Course",
        'width':150 
    },
    {
        "label":"Course Assessment Criteria",
        "fieldname":"assessment_criteria",
        "fieldtype":"Link",
        "options":"Course Assessment Criteria",
        'width':150
    },
    {
        "label":"Exam Assessment Plan",
        "fieldname":"assessment_plan",
        "fieldtype":"Link",
        "options":"Exam Assessment Plan",
        'width':150 
    },
    {
        "label":"Earned Marks",
        "fieldname":"earned_marks",
        "fieldtype":"float",
        'width':100
    },
    {
        "label":"Total Marks",
        "fieldname":"total_marks",
        "fieldtype":"Data",
        'width':100
    }
]

def get_data(filters):
    data = []
    fltr, flt2 = {},[]
    if filters.get("academic_year"):
        fltr.update({"academic_year":filters.get("academic_year")})
    if filters.get("academic_term"):
        fltr.update({"academic_term":filters.get("academic_term")})
    if filters.get("programs"):
        fltr.update({"programs":filters.get("programs")})
    if filters.get("assessment_criteria"):
        fltr.update({"assessment_criteria":filters.get("assessment_criteria")})
    if filters.get("course"):
        fltr.update({"course":filters.get("course")})
    if filters.get("semester"):
        fltr.update({"semester":filters.get("semester")})
        data = frappe.get_all('Course Assessment', filters=fltr,fields=['student', 'student_name','roll_no','academic_year', 'academic_term','programs','semester', 'course','assessment_criteria','assessment_plan', 'total_marks', 'earned_marks'])
    if filters.get("student_group"):
        stud_grp_list  = frappe.db.sql("""SELECT SGS.student from `tabStudent Group Student` as SGS 
        inner join  `tabStudent Group` as SG on SGS.parent = SG.name
        where SG.name = '{0}'""".format(filters.get("student_group"), as_list=1))
        if stud_grp_list:
            for row in data:
                if row.get('studpn ent') not in stud_grp_list:
                    data.remove(row)
    return data

@frappe.whitelist()
def get_course(doctype, txt, searchfield, start, page_len, filters):
    course_list=[]
    return frappe.get_all("Course Assessment",{"programs":filters.get('programs'),"semester":filters.get('semester')},["course"],as_list=1)

@frappe.whitelist()
def get_assessment_criteria(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Credit distribution List",{"parent":filters.get('course')},["assessment_criteria"],as_list=1)