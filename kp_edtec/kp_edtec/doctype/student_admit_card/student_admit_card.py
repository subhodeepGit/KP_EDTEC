# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate
from kp_edtec.kp_edtec.doctype.workspace import create_workspace
from kp_edtec.kp_edtec.utils import get_courses_by_semester,duplicate_row_validation

class StudentAdmitCard(Document):
    pass
    # def after_insert(self):
    #   create_workspace("Student",self.get('doctype'))

# bench execute kp_edtec.kp_edtec.doctype.student_admit_card.student_admit_card.create_admit_card
def create_admit_card():
    if frappe.db.get_single_value('Educations Configurations', 'exam_fee_applicable'):
        for exam_app in frappe.get_all("Exam Application",{"docstatus":1,'status':"Paid"}):
            exam=frappe.get_doc("Exam Application",exam_app.name)
            doc=frappe.new_doc("Student Admit Card")
            doc.registration_no=frappe.db.get_value("Program Enrollment",{"docstatus":1,"student":exam.student},'name')
            doc.student_roll_no=exam.student
            doc.student_name=exam.student_name
            doc.current_program=exam.current_program
            for e in exam.get('exam_application_courses'):
                exam_date=''
                from_time=''
                to_time=''
                for ap in frappe.get_all("Course Assessment Plan",{'program':exam.current_program,'course':e.course,'docstatus':1},['name','schedule_date','from_time','to_time']):
                    exam_date=ap.schedule_date
                    from_time=ap.from_time
                    to_time=ap.to_time
                doc.append("courses",{
                    'courses':e.course,
                    'examination_date':exam_date,
                    'from_time':from_time,
                    'to_time':to_time
                })
            if admit_card_not_exist(exam):
                doc.save()

def admit_card_not_exist(doc):
    return len(frappe.get_all("Student Admit Card",{"student_roll_no":doc.student,"current_program":doc.current_program}))==0

@frappe.whitelist()
def get_exam_details(program,student,academic_year,academic_term):
    result=[]
    exam_app = frappe.get_all("Exam Application",{'current_program':program,"program_academic_year":academic_year,"student":student,"academic_term":academic_term,"docstatus":1})
    if exam_app:
        for d in exam_app:
            course_details =  []
            doc=frappe.get_doc("Exam Application",d.name)
            for course in doc.get('exam_application_courses'):
                for ex in frappe.get_all("Exam Courses",{"parent":doc.get("exam_declaration"),"courses":course.course},["courses",'examination_date',"from_time","to_time","total_duration_in_hours","semester"]):
                    for cr in frappe.db.get_all('Course', {'name':course.course}, ['name','course_code','course_name']):
                        ex.update(cr)
                        result.append(ex)
        return result
    else:
        frappe.msgprint("Exam Application not found")

@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    courses=get_courses_by_semester(filters.get("program"))
    if courses:
        return frappe.db.sql("""select name,course_name,course_code from tabCourse
			where name in ({0}) and (name LIKE %s or course_name LIKE %s or course_code LIKE %s)
			limit %s, %s""".format(", ".join(['%s']*len(courses))),
			tuple(courses + ["%%%s%%" % txt, "%%%s%%" % txt,"%%%s%%" % txt, start, page_len]))
    return []