# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeAppraisal(Document):
    def validate(self):
        validate_date(self)
        set_total_score(self)

def validate_date(doc):
    if doc.start_date and doc.end_date and doc.end_date < doc.start_date:
        frappe.throw("End date should be greater than start date.")

def set_total_score(doc):
    criteria_list = []
    calculate_criteria_total(doc, "published_paper", criteria_list)
    calculate_criteria_total(doc, "seminars_and_guest_lecture", criteria_list)
    calculate_criteria_total(doc, "additional_resources", criteria_list)
    calculate_criteria_total(doc, "innovative_teaching_learning", criteria_list)
    calculate_criteria_total(doc, "article_and_chapters_published", criteria_list)
    calculate_criteria_total(doc, "conference__proceedings", criteria_list)
    calculate_criteria_total(doc, "book_published", criteria_list)
    calculate_criteria_total(doc, "research_project_and_consultancies", criteria_list)
    calculate_criteria_total(doc, "research_guidance", criteria_list)
    calculate_criteria_total(doc, "instructor_development_program", criteria_list)
    calculate_criteria_total(doc, "paper_presented", criteria_list)
    calculate_criteria_total(doc, "invited_lecture_and_chairmanship", criteria_list)
    calculate_criteria_total(doc, "ict_mediated_teaching_learning_pedagogy_and_content", criteria_list)
    calculate_criteria_total(doc, "design_of_new_curriculum_and_course", criteria_list)
    calculate_criteria_total(doc, "moocs", criteria_list)
    calculate_criteria_total(doc, "e_content", criteria_list)
    calculate_criteria_total(doc, "patent", criteria_list)
    calculate_criteria_total(doc, "policy_document", criteria_list)
    calculate_criteria_total(doc, "awards_and_fellowship", criteria_list)
    calculate_criteria_total(doc, "invited_lecture_and_chairmanship", criteria_list)

def calculate_criteria_total(doc, child_table, criteria_list):
    total_score = 0
    if len(doc.get(child_table)) > 0 :
        df = frappe.get_meta(doc.doctype).get_field(child_table)
        for row in doc.get(child_table):
            if row.score:
                total_score += row.score
        if total_score > 0:
            row_dict = {'criteria': df.label, 'score': total_score}
            criteria_list.append(row_dict)
        set_criteria_total(doc, criteria_list)

def set_criteria_total(doc, criteria_list):
    doc.summary_of_scores = []
    for row_dict in criteria_list:
        row = doc.append('summary_of_scores', {})
        row.criteria = row_dict['criteria']
        row.final_score = row_dict['score']
              
@frappe.whitelist()
def get_academic_courses(employee,academic_year):
    instructor = frappe.db.get_value("Instructor",{"employee":employee},"name")
    course_list = []
    if instructor :
       courses = frappe.db.get_list("Instructor Log",{'academic_year':academic_year,'parent':instructor}, ['course', "course_code", "course_name"])
       course_list = list({v['course']:v for v in courses}.values())
       total_hrs =  0
       for course in course_list:
          cs_data = frappe.db.get_all("Course Schedule",{"course":course.get('course'), "instructor":instructor},["from_time", "to_time", "name","schedule_date" ])
          if cs_data:
            hrs, class_attended, total_hrs =  0, 0, 0
            for cs in cs_data:
                time_diff = cs.get('to_time') - cs.get('from_time')
                hrs = time_diff.seconds//3600
                total_hrs += hrs
                stud_attend_data = frappe.db.get_all("Student Attendance",{"docstatus":1,"course_schedule":cs.name, "date":cs.schedule_date},["name"])
                if len(stud_attend_data):
                    class_attended += 1
            classes_taken = (class_attended* 100)/len(cs_data)
            if classes_taken >= 80:
                grade = "Good"
            elif classes_taken >= 70:
                grade = "Satisfactory"
            else:
                grade = "Not satisfactory"
            course.update({'hrs':total_hrs,'class_attended':class_attended,'classes_taken': round(classes_taken, 2), 'score':grade})
       return course_list
