# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from re import split
import frappe,json
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.background_jobs import enqueue
from kp_edtec.kp_edtec.utils import date_greater_than_or_equal,academic_term,semester_belongs_to_programs,get_courses_by_semester,duplicate_row_validation
from frappe.utils import flt
from kp_edtec.kp_edtec.notification.custom_notification import exam_declaration_submit,exam_declaration_for_instructor_submit
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission
from pytz import all_timezones, country_names
from frappe.utils.data import nowtime
from frappe.utils import cint, flt, cstr
from frappe import _


class ExamDeclaration(Document):
    def date_validation(self):
        if self.is_application_required:
            date_greater_than_or_equal(self,"application_form_start_date","application_form_end_date")

            if (self.application_form_start_date  >= self.exam_start_date) or (self.application_form_end_date  >=  self.exam_start_date):
                frappe.throw("<b>Exam Start Date</b> Should be Greater than <b>Application Start Date/End Date</b>")

            if self.block_list_display_date and self.application_form_end_date <= self.block_list_display_date:
                frappe.throw("<b>Block List Display Date</b> Should be Before <b>Application Start Date</b>")

            if self.admit_card_issue_date and (self.admit_card_issue_date<self.application_form_end_date or self.exam_start_date<=self.admit_card_issue_date):
                frappe.throw("<b>Admit Card Issue Date</b> Should be Less than <b>Application End Date</b> and Greater than <b>Exam Start Date</b>")

        for d in self.get("courses_offered"):
            if d.examination_date and (d.examination_date  < self.exam_start_date or d.examination_date  >  self.exam_end_date):
                frappe.throw("<b>Examination Date</b> Should be Greater than <b>Exam Start Date</b> and Less than <b>Exam End Date</b>")
    def calculate_total_hours(self):
        for d in self.get("courses_offered"):
            if d.to_time and d.from_time:
                d.total_duration_in_hours = datetime.strptime(d.to_time, '%H:%M:%S') - datetime.strptime(d.from_time, '%H:%M:%S')  
    def validate_courses(self):
        for cr in self.get("courses_offered"):
            if cr.courses and cr.courses not in get_courses_by_semester([d.semester for d in self.semesters]):
                frappe.throw("Course <b>{0}</b> not belongs to <b>Semesters</b>".format(cr.courses))

            if flt(cr.from_time)>flt(cr.to_time):
                frappe.throw("Row <b>{0}</b> From Time cannot be greater than To Time".format(cr.idx))

            # for duplicate in self.get("courses_offered"):
            #     if cr.courses == duplicate.courses and cr.idx != duplicate.idx:
            #         frappe.throw("Duplicate Course Not Allowed <b>{0}</b>".format(cr.courses)) 
    def validate_fee_structure(self):
        for fee in self.get("fee_structure"):
            if fee.fee_structure:

                if len(frappe.get_all("Fee Structure",{"name":fee.fee_structure,"programs":self.exam_program},['name']))==0:
                    frappe.throw("Fee Structure <b>{0}</b> Not belongs to <b>Exam Program</b>".format(fee.fee_structure))

                for struct in frappe.get_all("Fee Structure",{"name":fee.fee_structure},['fee_type']):
                    if struct.fee_type!="Exam Fees":
                        frappe.throw("Fee Structure <b>{0}</b> Should be of <b>Exam Fees</b>".format(fee.fee_structure)) 
    def sort_by_date(self):
        sorted_by_date = enumerate(sorted((self.get("courses_offered")), key = lambda date:date.get('examination_date')))
        self.courses_offered=[]
        for i,d in sorted_by_date:
            row = self.append('courses_offered', {})
            row.update({'courses':d.courses, 'examination_date':d.examination_date, 'from_time':d.from_time, 'to_time':d.to_time, 'semester':frappe.db.get_value('Program Course', {'course': d.courses,"parent":["IN",[d.semester for d in self.semesters]]}, 'parent'), 'course_name':d.course_name,'course_code':d.course_code, 'total_duration_in_hours':d.total_duration_in_hours})                           #                      
    @frappe.whitelist()
    def get_courses(self):
        course_list = get_courses_by_semester([d.semester for d in self.semesters])
        result = []
        for course in course_list:
            row = {}
            course_details = frappe.db.get_all('Course', {'name':course}, ['name','course_code','course_name'])
            semester = frappe.db.get_value('Program Course', {'course': course,"parent":["IN",[d.semester for d in self.semesters]]}, 'parent')
            course_details[0].update({'semester': semester})
            row.update(course_details[0])
            result.append(row)
        return result      
        return get_courses_by_semester([d.semester for d in self.semesters])
    def validate(self):
        self.date_validation()
        self.calculate_total_hours()
        self.validate_courses()
        self.validate_fee_structure()
#       self.validate_assessment_plan()
        academic_term(self)
        semester_belongs_to_programs(self)
        date_greater_than_or_equal(self,"exam_start_date","exam_end_date")
        duplicate_row_validation(self, "semesters", ['semester',])
        duplicate_row_validation(self, "courses_offered", ['courses','examination_date'])
        self.sort_by_date()
        # generate_fee(self)
    def set_user_permission(self):
        for il in frappe.get_all("Instructor Log",{"programs":self.exam_program},['parent']):
            for i in frappe.get_all("Instructor",{"name":il.parent},['employee']):
                if i.get('employee'):
                    for emp in frappe.get_all("Employee", {'name':i.get('employee')}, ['user_id']):
                        if emp.get('user_id'):
                            add_user_permission("Exam Declaration",self.name, emp.get('user_id'), self)
                        else:
                            frappe.msgprint("User Id is not created for employee {0} ".format(emp.employee_name))
                else:
                    frappe.msgprint("Instructor {0} is not employee".format(il.parent))

    def on_update_after_submit(self):
        self.sort_by_date()

    def on_trash(self): 
        self.delete_permission()

    def delete_permission(self):
        for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
            frappe.delete_doc("User Permission",d.name)

    def on_submit(self):
        self.set_user_permission()
        exam_declaration_submit(self)
        exam_declaration_for_instructor_submit(self)
        # self.make_exam_assessment_result()
        # fee_structure_id = fee_structure_validation(self)
        # create_fees(self,fee_structure_id,on_submit=1) 
        # on_update(self,on_submit=1)
    # def on_cancel(doc):
    #     cancel_fees(doc)

    
    def validate_assessment_plan(self):
        if self.course_assessment_plan:
            semesters=[]
            for d in self.get("semesters"):
                semesters.append(d.semester)
            if self.course_assessment_plan not in [d.name for d in frappe.get_all("Course Assessment Plan",{"programs":self.exam_program,"program":["IN",semesters],"academic_year":self.academic_year,"docstatus":1})]:
                frappe.throw("Please select valid <b>Course Assessment Plan</b>")    
#     @frappe.whitelist()
#     def make_exam_assessment_result(self):
#         self.db_set("certificate_creation_status", "In Process")
#         frappe.publish_realtime("exam_declaration_progress",
#             {"progress": "0", "reload": 1}, user=frappe.session.user)

#         total_records = len(self.get("students"))
#         if total_records > 35:
#             frappe.msgprint(_(''' Records will be created in the background.
#                 In case of any error the error message will be updated in the Schedule.'''))
#             enqueue(create_conduct_certificate, queue='default', timeout=6000, event='create_conduct_certificate',
#                 exam_declaration=self.name)

#         else:
#             create_conduct_certificate(self.name)
            
# def create_conduct_certificate(exam_declaration):
#     print("exam_declaration",exam_declaration)
#     doc = frappe.get_doc("Exam Declaration", exam_declaration)
#     error = False
#     total_records = len(doc.get("students"))
#     created_records = 0
#     if not total_records:
#         frappe.throw(_("Please setup Students under Student Groups"))
#     for d in doc.get("students"):
#         # try:
#         result=frappe.new_doc("Fees")
#         result.student=d.student
#         result.student_name=d.student_name
#         result.roll_no=d.roll_no
#         result.registration_number=d.registration_number
#         for enroll in frappe.get_all("Program Enrollment",{"student":d.student,"docstatus":1,"academic_term":doc.academic_term},['programs','program','academic_term','academic_year'],order_by="creation desc",limit=1):
#             result.programs=enroll.programs
#             result.program=enroll.program
#             result.program_enrollment=enroll.name
#         for fee_stu in doc.get("fee_structure"):
#             result.fee_structure=fee_stu.fee_structure
#             result.due_date=fee_stu.due_date
#             ref_details = frappe.get_all("Fee Component",{"parent":fee_stu.fee_structure},['fees_category','amount','receivable_account','income_account','company','grand_fee_amount','outstanding_fees'])
#             for i in ref_details:
#                 result.append("components",{
#                         'fees_category' : i['fees_category'],
#                         'amount' : i['amount'],
#                         'receivable_account' : i['receivable_account'],
#                         'income_account' : i['income_account'],
#                         'company' : i['company'],
#                         'grand_fee_amount' : i['grand_fee_amount'],
#                         'outstanding_fees' : i['outstanding_fees'],
#                     })

#             # result.program_enrollment=enroll.name
#         result.academic_year=doc.academic_year
#         result.academic_term=doc.academic_term
            
#         result.submit()
#         created_records += 1
#     frappe.msgprint("Record Created")
# def cancel_fees(doc):
#     for d in 
# 	exam_fee_object= frappe.get_doc("Fees",doc.fee_structure)
# 	exam_fee_object.cancel()

@frappe.whitelist()
def create_student_admit_card(self):
    make_student_admit_card(self)     

@frappe.whitelist()
def get_students(academic_term=None, programs=None):
    enrolled_students = get_program_enrollment(academic_term,programs)
    if enrolled_students:
        student_list = []
		
        for s in enrolled_students:
            if frappe.db.get_value("Student", s.student, "enabled"):
                s.update({"active": 1})
            else:
                s.update({"active": 0})
            student_list.append(s)
        return student_list
    else:
		
        frappe.msgprint("No students found")
        return []
def get_program_enrollment(academic_term,programs=None):
    condition1 = " "
    condition2 = " "
    if programs:
        condition1 += " and pe.programs = %(programs)s"
    return frappe.db.sql('''
        select
            pe.student, pe.student_name
        from
            `tabProgram Enrollment` pe {condition2}
        where
            pe.academic_term = %(academic_term)s  {condition1}
        order by
            pe.student_name asc
        '''.format(condition1=condition1, condition2=condition2),
                ({"academic_term": academic_term,"programs": programs}), as_dict=1) 
@frappe.whitelist()
def get_fee_structure(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Fee Structure",{"programs":filters.get("program"), "docstatus":1},['name','programs'],as_list = 1)

@frappe.whitelist()
def filter_courses(doctype, txt, searchfield, start, page_len, filters):
    courses=get_courses_by_semester(filters.get("program"))
    if courses:
        return frappe.db.sql("""select name,course_name,course_code from tabCourse
            where name in ({0}) and (name LIKE %s or course_name LIKE %s or course_code LIKE %s)
            limit %s, %s""".format(", ".join(['%s']*len(courses))),
            tuple(courses + ["%%%s%%" % txt, "%%%s%%" % txt,"%%%s%%" % txt, start, page_len]))
    return []

@frappe.whitelist()
def make_student_admit_card(doc):
    fltr = {'programs':doc.exam_program,'academic_year':doc.academic_year,'academic_term':doc.academic_term}
    student_list = frappe.db.get_all("Current Educational Details",fltr ,['semesters','parent'])
    if len(student_list) > 0:
        for stud in student_list:
            existing_record = [i.name for i in frappe.get_all("Fees",{'current_program':doc.exam_program,'academic_year':doc.academic_year,'academic_term':doc.academic_term,'student_roll_no':stud.parent},'name')]
            if len(existing_record)==0:
                program_enrollment = frappe.db.get_value("Program Enrollment",{'programs':doc.exam_program,'academic_year':doc.academic_year,'academic_term':doc.academic_term,'student':stud.parent, 'program':stud.semesters}, 'name')
                if program_enrollment:
                    sac =frappe.new_doc("Fees")
                    sac.academic_year=doc.academic_year
                    sac.academic_term=doc.academic_term
                    sac.current_program=doc.exam_program
                    sac.registration_no = program_enrollment
                    sac.student_roll_no = stud.parent
                    sac.student_name = frappe.db.get_value("Student",stud.parent,'title')
                    sac.set("courses",[])
                    for course in doc.courses_offered:
                        sac.append("courses",{
                            'courses':course.courses,
                            'course_name':course.course_name,
                            'course_code':course.course_code,
                            'semester':course.semester,
                            'examination_date':course.examination_date,
                            'from_time':course.from_time,
                            'to_time':course.to_time,
                            'total_duration_in_hours':course.total_duration_in_hours
                        })
                    sac.save()
                    frappe.msgprint("Fees <b>{0}</b> is created successfully".format(sac.name))
                else:
                    frappe.msgprint("Program Enrollment not found for student {0}".format(stud.parent))
            else:
                frappe.msgprint("Admit card is exit for student {0}".format(stud.parent))
    else :
        frappe.msgprint("Students not found.")

