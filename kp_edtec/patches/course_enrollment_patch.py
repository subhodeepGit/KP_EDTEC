import frappe

def execute():
    mapping_from_program_enrollment()

def mapping_from_program_enrollment():
    for cr_enroll in frappe.get_all("Course Enrollment",['name','program_enrollment']):
        course_enrollment=frappe.get_doc("Course Enrollment",cr_enroll.name)
        for pr_enroll in frappe.get_all("Program Enrollment",{"name":cr_enroll.program_enrollment},['academic_year','academic_term','program']):
            course_enrollment.academic_year=pr_enroll.acdemic_year
            course_enrollment.academic_term=pr_enroll.academic_term
            course_enrollment.program=pr_enroll.program
            for cr in frappe.get_all("Course",{"name":course_enrollment.course},['course_name','course_code']):
                course_enrollment.course_name=cr.course_name
                course_enrollment.course_code=cr.course_code
            course_enrollment.save()