# -*- coding: utf-8 -*-
# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission
from frappe.utils import today
from kp_edtec.kp_edtec.notification.custom_notification import branch_change_declaration_submit

class BranchslidingDeclaration(Document):
    def validate(self):
        self.validate_programs()
        self.validate_duplicate_program()
        self.validate_seats()
        self.duplicate_branch_change_declaration()
        self.date_validation()

    def on_submit(self):
        branch_change_declaration_submit(self)
        self.share_document()

    def on_cancel(self):
        self.delete_share_document()

    def share_document(self):
        duplicate_enroll=[]
        for pe in frappe.get_all("Program Enrollment",{"docstatus":1,"programs":self.for_program},["student"]):
            if pe.student not in duplicate_enroll:
                for d in self.get("branch_sliding__criteria"):  
                    add_user_permission("Programs",d.program, frappe.db.get_value("Student",{"name":pe.student},"student_email_id"),self)

            duplicate_enroll.append(pe.student)
        
    def delete_share_document(self):
        for d in frappe.get_all("User Permission",{"reference_doctype":self.doctype,"reference_docname":self.name}):
            frappe.delete_doc("User Permission",d.name)

    def date_validation(self):   
        if self.application_start_date and self.application_end_date and self.application_start_date > self.application_end_date:
            frappe.throw("Application End Date should be Greater than Application Start date")
            
    def validate_programs(self):
        department=frappe.db.get_value("Programs",{"name":self.for_program},"department")

        for criteria in self.get("branch_sliding__criteria"):
            if frappe.db.get_value("Programs",{"name":criteria.program},"department") != department:
                frappe.throw("<b>For Program</b> Department <b>Criteria Programs</b> Department Must be Same")

            if criteria.program==self.for_program:
                frappe.throw("<b>Criteria Programs</b> should not be equal to <b>For Program</b>")
    
    def duplicate_branch_change_declaration(self):
        existing_record = [b.name for b in frappe.db.get_all("Branch sliding Declaration",{"for_program":self.for_program, 'academic_year':self.academic_year, 'docstatus':1},"name")]
        if len(existing_record) > 0 :
            existing_record = ' '.join([str(elem) for elem in existing_record])
            frappe.throw("Record is exist in <b>{0}</b> for program and academic year".format(existing_record))

    def validate_duplicate_program(self):
        for criteria in self.get("branch_sliding__criteria"):
            for duplicate in self.get("branch_sliding__criteria"):
                if criteria.program == duplicate.program and criteria.idx != duplicate.idx:
                    frappe.throw("Duplicate Programs <b>{0}</b> Not Allowed".format(criteria.program))

    def validate_seats(self):
        for criteria in self.get("branch_sliding__criteria"):
            
            # negative value
            if criteria.total_seats < 0 or criteria.available_seats < 0:
                frappe.throw("Seats Value Must be <b>Positive</b>")

            # total value should be greater
            if criteria.total_seats < criteria.available_seats:
                frappe.throw("<b>Available Seats</b>  Should be Less than or Equal to <b>Total Seats</b>")

@frappe.whitelist()
def get_programs(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""SELECT name 
                                    from `tabPrograms` 
                            WHERE name!='{0}' 
                            and (name like '%{2}%') 
                            and department='{1}'"""
            .format(filters.get("programs"),frappe.db.get_value("Programs",{"name":filters.get("programs")},"department"), txt))


@frappe.whitelist()
def get_semesters(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Semesters", {'parent':filters.get('programs')},['semesters'],as_list=1)
    
     # for d in frappe.get_all("Mentor Allocation",{"mentor":filters.get("mentor")},["name"]):
     #    return frappe.get_all("Mentee List",{"parent":d.name},['student'],as_list=1)

    # return frappe.db.sql("""SELECT name 
    #                               from `tabPrograms` 
    #                       WHERE name!='{0}' 
    #                       and (name like %(txt)s) 
    #                       and department='{1}'"""
    #       .format(filters.get("programs"),frappe.db.get_value("Programs",{"name":filters.get("programs")},"department")),{'txt': '%%%s%%' % txt})
