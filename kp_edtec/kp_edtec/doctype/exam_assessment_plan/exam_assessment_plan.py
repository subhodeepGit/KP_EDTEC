  # Copyright (c) 2022, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import today,getdate
from kp_edtec.kp_edtec.utils import duplicate_row_validation,get_courses_by_semester
# from kp_edtec.kp_edtec.notification.custom_notification import exam_evaluation_plan_for_paper_setter_submit,exam_evaluation_plan_for_moderator_submit

class ExamAssessmentPlan(Document):
    def validate(self):
        self.validate_exam_declaration()
        self.validate_dates()
        self.validate_programs()
        self.validate_semester()
        self.validate_course()
        duplicate_row_validation(self,"examiners_list",["paper_setter","course"])
        duplicate_row_validation(self,"moderator_list",["moderator","course"])
    
    # def on_submit(self):
    #     exam_evaluation_plan_for_paper_setter_submit(self)
    #     exam_evaluation_plan_for_moderator_submit(self)

    @frappe.whitelist()
    def create_exam_paper_setter(self):
        make_exam_paper_setting(self)

    def validate_programs(self):
        for declaration in frappe.get_all("Exam Declaration",{"name":self.exam_declaration},['exam_program']):
            if declaration.exam_program != self.programs:
                frappe.throw("<b>Programs</b> not belongs to <b>Exam Declaration</b>")

    def validate_semester(self):
        if self.program not in [d.semester for d in frappe.get_all("Examination Semester",{"parent":self.exam_declaration},['semester'])]:
            frappe.throw("<b>Semester</b> not belongs to <b>Exam Declaration</b>")

    def validate_exam_declaration(self):
        if self.exam_declaration and self.exam_declaration not in [d.name for d in frappe.get_all("Exam Declaration",{"docstatus":1,"disabled":0})]:
            frappe.throw("Please Select Valid <b>Exam Declaration</b>")

    def validate_dates(self):
        if (self.paper_setting_start_date  and self.paper_setting_end_date and self.paper_setting_start_date > self.paper_setting_end_date):
            frappe.throw("Start Date should be less than End Date")

        # if (self.paper_setting_start_date and self.paper_setting_start_date < today()):
        #     frappe.throw("Start Date should be greater than today's date")

    def validate_course(self):
        courses=[d.parent for d in frappe.get_all("Credit distribution List",{"assessment_criteria":self.get("assessment_criteria"),"parent":["IN",get_courses_by_semester(self.get("program"))]},['parent'],group_by="parent")]
        lst=[]
        if courses:
            lst=[d.courses for d in frappe.get_all("Exam Courses",{"parent":self.get("exam_declaration"),"courses":["IN",courses]},["courses"])]
            # for cr in frappe.db.sql("""select cr.name,cr.course_name from `tabCourse` cr left join `tabAdmit Card Course` decl_course on decl_course.courses=cr.name where cr.name in ({0}) and decl_course.parent='{1}'""".format(", ".join(['%s']*len(courses)),self.get("exam_declaration"))):
            #   lst.append(cr.name)
        for cr in self.get("course_assessment_plan_item"):
            if cr.course not in lst:
                frappe.throw("Please Select Valid <b>Course</b> In Exam Assessment Plan Item")

            for duplicate in self.get("course_assessment_plan_item"):
                if cr.course == duplicate.course and cr.idx!=duplicate.idx:
                    frappe.throw("Duplicate Course Not Allowed <b>{0}</b>".format(cr.course))

        for cr in self.get("moderator_list"):
            # if cr.course not in lst:
            #   frappe.throw("Please Select Valid <b>Course</b> In Moderator List")
            
            if cr.course not in [d.course for d in self.get("course_assessment_plan_item")]:
                frappe.throw("Course <b>{0}</b> not exist in Exam Assessment Plan Item".format(cr.course))

        for cr in self.get("examiners_list"):
            # if cr.course not in lst:
            #   frappe.throw("Please Select Valid <b>Course</b> In Examiners List")

            if cr.course not in [d.course for d in self.get("course_assessment_plan_item")]:
                frappe.throw("Course <b>{0}</b> not exist in Exam Assessment Plan Item".format(cr.course))
                

@frappe.whitelist()
def get_sem(doctype, txt, searchfield, start, page_len, filters):
    semesters=[]
    for sem in frappe.get_all("Examination Semester",{"parent":filters.get("exam_declaration")},['semester']):
        for s in frappe.get_all("Program",{"name":sem.semester},["*"],as_list=1):
            semesters.append(s)
    return semesters

@frappe.whitelist()
def filter_paper_setter(doctype, txt, searchfield, start, page_len, filters):
    fltr, instructor_list = {},[]
    if filters:
        fltr.update({"course":filters.get("course")})
    instructor_list = frappe.get_all("Instructor Log",fltr,'parent', as_list=1)
    if len(instructor_list) > 0:
        for i in instructor_list:
            emp_list = frappe.get_list("Instructor", {'name':i,'name': ['like', '%{}%'.format(txt)], 'employee': ['like', '%{}%'.format(txt)]}, ['employee','name'])
            return [[e.name, e.employee] for e in emp_list if len(emp_list)> 0]
    else:
        return []
        frappe.msgprint("Instructor not found for the course {0}".format(filters.get("course")))
        
@frappe.whitelist()
def course_assessment_credit(student_group):
    data=[]
    for sg in frappe.get_all("Student Group",{"name":student_group},["exam_declaration"]):
        for crs in frappe.get_all("Admit Card Course",{"parent":sg.exam_declaration},["courses"]):
            for credit in frappe.get_all("Course Credit",{"parent":crs.courses},["total"]):
                crs.update(credit)
            data.append(crs)
    return data

@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    courses=[d.parent for d in frappe.get_all("Credit distribution List",{"assessment_criteria":filters.get("assessment_criteria"),"parent":["IN",get_courses_by_semester(filters.get("program"))]},['parent'],group_by="parent")]
    if courses:
        return frappe.db.sql("""select cr.name,cr.course_name,cr.course_code from `tabCourse` cr left join `tabExam Courses` decl_course on decl_course.courses=cr.name
            where cr.name in ({0}) and (cr.name LIKE %s or cr.course_name LIKE %s or cr.course_code LIKE %s) and decl_course.parent='{1}' and decl_course.semester='{2}'
            limit %s, %s""".format(", ".join(['%s']*len(courses)),filters.get("exam_declaration"),filters.get("program")),
            tuple(courses + ["%%%s%%" % txt, "%%%s%%" % txt, start, page_len]))
    return []
    
@frappe.whitelist()
def get_assessment_criteria_detail(course,criteria):
    for data in frappe.get_all("Credit distribution List",{"parent":course,"assessment_criteria":criteria},["credits","total_marks","passing_marks"]):
        return data


@frappe.whitelist()
def get_courses_by_paper_setter(doctype, txt, searchfield, start, page_len, filters):
    courses=[]
    for i in frappe.get_all("Instructor Log",{"parent":filters.get("paper_setter")},["course"]):
        for cr in frappe.get_all("Course",{"name":i.course},["*"],as_list=1):
            courses.append(cr)
    return courses

def make_exam_paper_setting_by_paper_setting_date():
    for cp in frappe.get_all("Exam Assessment Plan",{"paper_setting_start_date":getdate(today())}):
        doc=frappe.get_doc("Exam Assessment Plan",cp.name)
        make_exam_paper_setting(doc)

def make_exam_paper_setting(doc):
    for ex in doc.get("examiners_list"):
        existing_record = [i.name for i in frappe.get_all("Exam Paper Setting",{"examiner":ex.paper_setter,"academic_year":doc.academic_year,"academic_term":doc.academic_term,"course":ex.course,"programs":doc.programs,"program":doc.program,"assessment_plan":doc.name},'name')]
        if len(existing_record)==0:
            for i in range(ex.no_of_sets):
                eps=frappe.new_doc("Exam Paper Setting")
                eps.examiner=ex.paper_setter
                eps.academic_year=doc.academic_year
                eps.academic_term=doc.academic_term
                eps.course=ex.course
                eps.assessment_plan=doc.name
                eps.programs=doc.programs
                eps.program=doc.program
                for moderator in doc.get("moderator_list"):
                    if moderator.course==ex.course:
                        eps.moderator_name=moderator.moderator
                eps.save()
                frappe.msgprint("Exam Paper Setting <b>{0}</b> is created successfully".format(eps.name))
        else :
            frappe.msgprint("Exam Paper Setting <b>{0}</b> is already exist".format(' '.join(map(str, existing_record))))
    return "ok"