# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today,getdate
from kp_edtec.kp_edtec.utils import get_courses_by_semester
# from kp_edtec.kp_edtec.notification.custom_notification import branch_change_application_applied,branch_change_application_approved,branch_change_application_rejected

class BranchSlidingApplication(Document):
    def validate(self):
        start_date = frappe.db.sql("""SELECT count(B.name) as length
        from `tabBranch sliding Declaration` as B inner join `tabBranch Sliding Item` as BI 
        on B.name = BI.parent where B.docstatus=1 and B.academic_year = '{0}' 
        and B.application_start_date > CURDATE() and BI.program='{1}' and B.name = '{2}'
        """.format(self.academic_year, self.sliding_in_program, self.branch_sliding_declaration), as_dict=1)
       
        end_date = frappe.db.sql("""SELECT count(B.name) as length
        from `tabBranch sliding Declaration` as B inner join `tabBranch Sliding Item` as BI 
        on B.name = BI.parent where B.docstatus=1 and B.academic_year = '{0}' 
        and B.application_end_date < CURDATE() and BI.program='{1}' and B.name = '{2}'
        """.format(self.academic_year, self.sliding_in_program, self.branch_sliding_declaration), as_dict=1)
       
        if start_date[0] and start_date[0]['length'] > 0:
            frappe.throw("Application start not start yet on Branch sliding declaration. So, you are not eligible for apply.")
        if end_date[0] and end_date[0]['length'] > 0:
             frappe.throw("Application date is end on Branch sliding declaration.So, you are not eligible for apply.")
        
        for bsd in frappe.get_all("Branch sliding Declaration",{"academic_year":self.academic_year,"application_start_date":("<",today()),"application_end_date":(">=",today()),"docstatus":1}):
            for bsdi in frappe.get_all("Branch Sliding Item",{"program":self.sliding_in_program,"parent":bsd.name},['eligibility_score','available_seats']):
                if self.last_year_score < bsdi.eligibility_score:
                    frappe.throw("<b>Last Year Score </b> Not Eligible")
                if bsdi.available_seats < 1:
                    frappe.throw("<b>Seats</b> Not Avalible")
        date_validation(self)       

    # def on_change(self):
    #     if self.docstatus==1 and self.status=="Applied":
    #         branch_change_application_applied(self)
    #     elif self.docstatus==1 and self.status=="Approved":
    #         branch_change_application_approved(self)
    #     elif self.docstatus==1 and self.status=="Rejected":
    #         branch_change_application_rejected(self)

@frappe.whitelist()
def get_student_details(student):
    for pe in frappe.get_all("Program Enrollment",filters={"student":student, "docstatus":1},fields=['academic_year','programs'],order_by="creation desc",limit=1):
        pe.update({"declaration":frappe.db.get_value("Branch sliding Declaration",{"for_program":pe.get("programs"),'docstatus':1})})
        return pe.update({"semester":frappe.db.get_value("Branch Sliding Item",{"parent":pe.get("declaration")}, 'semester')})
    return {}

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_sliding_in_progam(doctype, txt, searchfield, start, page_len, filters):
    fltr = {"parent":filters.get("branch_sliding_declaration")}
    lst = []
    if txt:
        fltr.update({"program":['like', '%{}%'.format(txt)]})
    for i in frappe.get_all("Branch Sliding Item",fltr,['program']):
        if i.program not in lst:
            lst.append(i.program)
    return [(d,) for d in lst]

@frappe.whitelist()
def enroll_student(source_name):
    doc=frappe.get_doc("Branch Sliding Application",source_name)
    student=frappe.get_doc("Student",doc.student)
    program_enrollment = frappe.new_doc("Program Enrollment")
    program_enrollment.student = student.name
    program_enrollment.student_category = student.student_category
    program_enrollment.student_name = student.title
    program_enrollment.reference_doctype="Branch Sliding Application"
    program_enrollment.reference_name=source_name
    program_enrollment.programs = doc.sliding_in_program
    program_enrollment.program_grade=frappe.db.get_value("Programs",{"name":doc.sliding_in_program},"program_grade")
    program_enrollment.academic_year=doc.academic_year
    program_enrollment.program = doc.sliding_in_semester
    for cr in get_courses_by_semester(doc.sliding_in_semester):
        program_enrollment.append("courses",{
            "course":cr,
            "course_name":frappe.db.get_value("Course",{"name":cr},"course_name")
        })
    if get_academic_events(doc.sliding_in_program,doc.sliding_in_semester, doc.academic_year):
        for event in get_academic_events(doc.sliding_in_program,doc.sliding_in_semester, doc.academic_year):
            program_enrollment.append("academic_events_table",{
                "academic_events" : event.academic_events,
                "start_date" : event.start_date,
                "end_date" : event.end_date,
                "duration" : event.duration
            })
    if doc.branch_sliding_declaration:
        for seat in [s.available_seats for s in frappe.get_all("Branch Sliding Item",{"parent":doc.branch_sliding_declaration},'available_seats')]:
            program_enrollment.available_seats = seat
    return program_enrollment
    
def get_academic_events(programs,semester,academic_year):
    for d in [c.name for c in frappe.get_all("Academic Calendar Template",{"programs":programs,"program":semester, 'academic_year':academic_year}, 'name')]:
        return frappe.get_all("Academic Events Table",{'parent':d},['academic_events','start_date','end_date','duration'])

def date_validation(doc):
    if doc.branch_sliding_declaration:
        declaration=frappe.get_doc("Branch sliding Declaration",doc.branch_sliding_declaration)
        if (getdate(declaration.application_end_date)<getdate(doc.application_date) and getdate(declaration.application_start_date)<getdate(doc.application_date)) or (getdate(declaration.application_end_date)>getdate(doc.application_date) and getdate(declaration.application_start_date)>getdate(doc.application_date)):
            frappe.throw("Application Date Should be in Between Start and End Date of Declaration")

@frappe.whitelist()
def get_declaration_details(**args):
    for declaration in frappe.get_all("Branch Sliding Item",{"parent":args.get("branch_sliding_declaration"),"program":args.get("sliding_in_program"),"parenttype":"Branch sliding Declaration"},["semester"]):
        return declaration.semester
        
