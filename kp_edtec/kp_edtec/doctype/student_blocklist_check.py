# -*- coding: utf-8 -*-
# Copyright (c) 2020, bizmap technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today, getdate

#kp_edtec.kp_edtec.doctype.student_blocklist_check.student_blocklist_check

def student_blocklist_check():
    #programs>>

    for ed in frappe.get_all("Exam Declaration",['name','block_list_display_date','program','exam_program','minimum_attendance_criteria','academic_term']):
        if ed.get("block_list_display_date") == getdate(today()):
            doc=frappe.new_doc("Student Exam Block List")
            doc.program = ed.get("exam_program")
            doc.exam_declaration = ed.get("name")
            doc.semester = ed.get("program")
            std_lst = []
            for co in frappe.get_all("Exam Courses",{'parenttype':"Exam Declaration","parent":ed.get("name")},["courses"]):
                for cs in frappe.get_all("Course Schedule",{"course":co.get("courses")},['name','course','student_group']):
                    
                    for sgs in frappe.get_all('Student Group Student',{'parent':cs.get("student_group")},['student','student_name']):
                        stud = len(frappe.get_all("Student Attendance",{"student_name":sgs.get("student_name"),'student_group':cs.get("student_group"),"status":'Present',"docstatus":1}))
                        crs_sdl = len(frappe.get_all("Course Schedule",{"course":co.get("courses")}))
                        avg = (stud/crs_sdl)*100
                        if ed.get('minimum_attendance_criteria') > avg  and sgs.get("student") not in std_lst:
                        #if 75 > avg and sgs.get("student") not in std_lst:
                            
                            
                            doc.append("student_block_item",{
                                "student":sgs.get("student"),
                                "student_name": sgs.get("student_name")
                            })
                            std_lst.append(sgs.get("student"))
            doc.save()
                            
