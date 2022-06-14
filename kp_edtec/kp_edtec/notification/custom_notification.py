from re import L
import frappe
from frappe.utils.data import format_date
from frappe.utils import get_url_to_form
from frappe.utils import cint, cstr, parse_addr


def student_applicant_submit(doc):
    sub="""<p><b>Application Form is Sucessfully Submitted</b></p><br>"""
    msg+="""<b>---------------------Applicant Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}{1}<br>""".format(doc.get('first_name'), doc.get('last_name'))
    msg+="""<b>Application Number:</b>  {0}<br>""".format(doc.get('name'))
    msg+="""<b>Department:</b>  {0}<br>""".format(doc.get('department'))
    msg+="""<b>Program Grade:</b>  {0}<br>""".format(doc.get('program_grade'))
    msg+="""<p>Priority Programs: </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Programs</th>"""
    for d in doc.get("program_priority"):
        msg += """<tr><td>{0}</td></tr>""".format(str(d.get('programs'))) 
    msg += "</table>"
    send_mail(frappe.db.get_value("Student Applicant",doc.get('name'),"student_email_id"),'Application status',msg)

def program_enrollment_admitted(doc):
    msg="""<p>You are admitted in the Programs <b>{0}</b></p><br>""".format(doc.get('programs'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Student Batch:</b>  {0}<br>""".format(doc.get('student_batch_name') or '-')
    msg+="""<b>Permanent Registration Number:</b>  {0}<br>""".format(doc.get('permanant_registration_number') or '-' )
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('programs'))
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('program'))
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Academic Term:</b> {0}<br>""".format(doc.get('academic_term') or '-')
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application status',msg)

def program_enrollment_provisional_admission(doc):
    msg="""<p>You are Provisionaly Admitted in the Programs <b>{0}</b></p><br>""".format(doc.get('programs'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Student Batch:</b>  {0}<br>""".format(doc.get('student_batch_name') or '-')
    msg+="""<b>Permanent Registration Number:</b>  {0}<br>""".format(doc.get('permanant_registration_number') or '-' )
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('programs'))
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('program'))
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Academic Term:</b> {0}<br>""".format(doc.get('academic_term') or '-')

    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application status',msg)


def branch_change_declaration_submit(doc):
    msg="""<p>Branch Change for <b>{0}</b> has been declared </p><br>""".format(doc.get('for_program'))
    msg+="""<b>---------------Branch Change Declaration Details---------------</b><br>"""
    msg+="""<b>Branch Change Declaration ID:</b>  {0}<br>""".format(doc.get('name'))
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Application Start Date:</b>  {0}<br>""".format(format_date(doc.get('application_start_date'), 'dd/mm/yyyy'))
    msg+="""<b>Application End Date:</b>  {0}<br><br><br>""".format(format_date(doc.get('application_end_date'), 'dd/mm/yyyy'))
    msg+="""<b>Branch Change Criteria:</b><br>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Programs</th><th>Semester</th><th>Eligibility score</th><th>Available Seats</th>"""

    for d in doc.get("branch_sliding__criteria"):
        msg += "<tr><td>" + """{0}""".format(str(d.get('program'))) + "</td><td>" + str(d.get('semester')) + "</td><td>" + str(d.get('eligibility_score')) + "</td><td>" + str(d.get('available_seats'))  + "</td></tr>"
    
    msg += "</table>"

    for enroll in frappe.get_all("Program Enrollment",{"programs":doc.get('for_program'),"academic_year":doc.get('academic_year')},['student']):
        send_mail(frappe.db.get_value("Student",enroll.get('student'),"student_email_id"),'Branch Change Declaration',msg)

def branch_change_application_applied(doc):
    msg="""<p>Your application <b>{0}</b> for Branch Change is successfully submitted. </p><br>""".format(doc.get('name'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('sliding_in_program') or '-')
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('sliding_in_semester') or '-')
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application Status',msg)

def branch_change_application_approved(doc):
    msg="""<p>Your application <b>{0}</b> for Branch Change is Approved. </p><br>""".format(doc.get('name'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('sliding_in_program') or '-')
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('sliding_in_semester') or '-')
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application Status',msg)

def branch_change_application_rejected(doc):
    msg="""<p>Your application <b>{0}</b> for Branch Change is Rejected. </p><br>""".format(doc.get('name'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('sliding_in_program') or '-')
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('sliding_in_semester') or '-')
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))
    
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application Status',msg)

def mentor_allocation_submit(doc):
    # For Mentor
    msg="""<p>You have been assigned the mentees for this Academic Year <b>{0}</b></p><br>""".format(doc.get('academic_year'))
    msg+="""<b>-----------Mentor-Mentee Group Details-----------</b><br>"""
    msg+="""<b>Mentor Name:</b>  {0}<br>""".format(doc.get('mentor_name') or '-')
    msg+="""<b>Alloaction From:</b>  {0}<br>""".format(doc.get('allocation_from') or '-')
    msg+="""<b>Alloaction To:</b>  {0}<br>""".format(doc.get('allocation_to') or '-')
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('program') or '-')
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('semester') or '-')
    msg+="""<b>Student Table:</b>  <a href="{0}">Click here to see the students</a><br>""".format(get_url_to_form('Mentor Allocation',doc.get('name')))

    send_mail(frappe.db.get_value("Employee",doc.get('mentor'),"user_id"),'Mentor Allocation', msg)

    # For Student
    for st in doc.get("mentee_list"):
        msg="""<p>You have been assigned the Mentor for this Academic Year <b>{0}</b></p><br>""".format(doc.get('academic_year'))
        msg+="""<b>-----------Mentor-Mentee Group Details-----------</b><br>"""
        msg+="""<b>Mentor Name:</b>  {0}<br>""".format(doc.get('mentor_name') or '-')
        msg+="""<b>Alloaction From:</b>  {0}<br>""".format(doc.get('allocation_from') or '-')
        msg+="""<b>Alloaction To:</b>  {0}<br>""".format(doc.get('allocation_to') or '-')
        msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('program') or '-')
        msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('semester') or '-')
        msg+="""<b>Student Application No:</b> {0}<br>""".format(doc.get('name'))

        send_mail(frappe.db.get_value("Student",st.get('student'),"student_email_id"),'Mentor Allocation',msg)

def send_mail(recipients,subject,message):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients,subject=subject,message = message)
    
def has_default_email_acc():
    for d in frappe.get_all("Email Account", {"default_outgoing":1}):
       return "true"
    return ""

def exam_declaration_submit(doc):
    sub = "Exam has been declared for your program {0}".format(doc.exam_program)
    msg="""<p>--------Exam Details----------</p>"""
    msg+="""<p>Exam Declaration Id : {0}</p>""".format(doc.name)
    msg+="""<p>Exam Program : {0}</p>""".format(doc.exam_program)
    msg+="""<p>Application start date : {0}</p>""".format(doc.application_form_start_date)
    msg+="""<p>Application End Date : {0}</p>""".format(doc.application_form_end_date)
    msg+="""<p>Blocklist Date:{0}</p>""".format(doc.block_list_display_date)
    msg+="""<p>Admit Card Issue Date : {0}</p>""".format(doc.admit_card_issue_date)
    msg+="""<p>Exam Semester : </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Semester</th>"""
    for d in doc.get("semesters"):
        msg += """<tr><td>{0}</td></tr>""".format(str(d.get('semester'))) 
    msg += "</table>"
    if doc.exam_fees_applicable == "YES":
        msg+="""<p>Exam Fees : </p>"""
        msg += """</u></b></p><table class='table table-bordered'><tr>
            <th>Student Category</th><th>Fee Structure</th><th>Amount</th><th>Due Date</th>"""
        for d in doc.get("fee_structure"):
            msg += "<tr><td>" + """{0}""".format(str(d.get('student_category'))) + "</td><td>" + str(d.get('fee_structure') or '') + "</td><td>" + str(d.get('amount')) + "</td><td>" + str(d.get('due_date'))  + "</td></tr>"
        msg += "</table>"
    
    for s in frappe.db.get_all('Current Educational Details',{'programs': doc.exam_program,"semesters":["IN",[d.semester for d in doc.get("semesters")]],'academic_year': doc.academic_year, 'academic_term':doc.academic_term}, 'parent'):
        send_mail(frappe.db.get_value("Student",s.get('parent'),"student_email_id"),sub,msg)

def post_exam_declaration_save(doc):
    msg="""<p>--------Post Exam Details----------</p>"""
    msg+="""<p>Post Exam Declaration Id : {0}</p>""".format(doc.name)
    msg+="""<p>Exam Declaration Id : {0}</p>""".format(doc.exam_declaration)
    exam_declrn = frappe.db.get_all('Exam Declaration', {'name':doc.exam_declaration})
    ed_doc = frappe.get_doc('Exam Declaration',exam_declrn[0]['name'])
    exam_program = ''
    msg+="""<p>Exam Program : {0}</p>""".format(ed_doc.exam_program)
    msg+="""<p>Application start date : {0}</p>""".format(doc.start_date or "")
    msg+="""<p>Application End Date : {0}</p>""".format(doc.end_date or "")
    msg+="""<p>Exam Semester : </p>  """
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Semester</th>"""
    for d in ed_doc.get("semesters"):
        msg += """<tr><td>{0}</td></tr>""".format(str(d.get('semester'))) 
    msg += "</table>"
    if doc.fees_applicable == "YES":
        msg+="""<p>Exam Fees : </p>"""
        msg += """</u></b></p><table class='table table-bordered'><tr>
            <th>Student Category</th><th>Fee Structure</th><th>Amount</th><th>Due Date</th>"""
        for d in doc.get("fee_structure"):
            msg += "<tr><td>" + """{0}""".format(str(d.get('student_category'))) + "</td><td>" + str(d.get('fee_structure') or '') + "</td><td>" + str(d.get('amount')) + "</td><td>" + str(d.get('due_date'))  + "</td></tr>"
        msg += "</table>"
    sub = "Post Exam has been declared for your program {0}".format(ed_doc.exam_program)
    student_list = frappe.db.get_all('Program Enrollment',{'programs': ed_doc.exam_program}, 'student')
    for s in student_list:
        send_mail(frappe.db.get_value("Student",s.get('student'),"student_email_id"),sub,msg)

def student_exam_block_submit(doc):
    sub = "Exam has been declared for your program {0}".format(doc.program)
    msg="""<p>--------Exam Details----------</p>"""
    msg+="""<p>>Exam Declaration : {0}</p>""".format(doc.exam_declaration)
    msg+="""<p>Program of Exam : {0}</p>""".format(doc.program)
    exam_declrn = frappe.db.get_all('Exam Declaration', {'name':doc.exam_declaration})
    for e in exam_declrn:
        msg+="""<p>Academic Year : {0}</p>""".format(e.academic_year)
        msg+="""<p>Academic Term : {0}</p>""".format(e.academic_term)
    for s in doc.student_block_item:
        send_mail(frappe.db.get_value("Student",s.get('student'),"student_email_id"),sub,msg)

@frappe.whitelist()
def placement_drive_application_submit(doc):
    import json
    doc = json.loads(doc)
    student_email_id = frappe.db.get_value("Student",{'name':doc.get('student')}, "student_email_id")
    sub = "Application Status"
    if doc.get('status') == "Shortlisted":
        sub = "Your application {0} is shortlisted for placement drive {1}".format(doc.get('name'), doc.get('placement_drive'))
    if doc.get('status') == "Hired":
        sub = "Your application {0} is hired for placement drive {1}".format(doc.get('name'), doc.get('placement_drive'))
    if doc.get('status') == "Rejected":
        sub = "Your application {0} is rejected for placement drive {1}".format(doc.get('name'), doc.get('placement_drive'))
    msg="""<p>--------Student Details----------</p>"""
    msg+="""<p>Student Name : {0}</p>""".format(doc.get('student_name'))
    msg+="""<p>Student Email: {0}</p>""".format(student_email_id)
    msg+="""<p>Placement Drive Name: {0}</p>""".format(doc.get('placement_drive'))
    msg+="""<p>Status: {0}</p>""".format(doc.get('status'))
    send_mail(student_email_id, sub, msg)

def placement_drive_submit(doc):
    sub = "Placement Drive is declared for {0}".format(doc.placement_company)
    msg="""<p>--------Placement Drive Details----------</p>"""
    msg+="""<p>Company Name : {0}</p>""".format(doc.placement_company)
    msg+="""<p>Application Start Date : {0}</p>""".format(doc.application_start_date)
    msg+="""<p>Application End Date :{0}</p>""".format(doc.application_end_date)
    msg+="""<p>Position: </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
            <th>Designation</th><th>No. of Positions</th>"""
    for d in doc.get("designations_position"):
        msg += "<tr><td>" + """{0}""".format(str(d.get('designation'))) + "</td><td>" + str(d.get('no_of_position') or '') + "</td></tr>"
    msg += "</table>"
    msg+="""<p>Applicable Programs: </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
            <th>Programs</th><th>Semester</th>"""
    for d in doc.get("for_programs"):
        msg += "<tr><td>" + """{0}""".format(str(d.get('programs'))) + "</td><td>" + str(d.get('semester') or '') + "</td></tr>"
    msg += "</table>"
    msg+="""<p>Eligibility Criteria: {0}</p>""".format(doc.eligibility_criteria)
    msg+="""<p>Placement Process: {0}</p>""".format(doc.process_of_placement)
    for s in doc.for_programs:
        student_list = frappe.get_list("Current Educational Details",{'programs':s.programs, 'semesters':s.semester}, 'parent')
        for stud in student_list:
            send_mail(frappe.db.get_value("Student",stud.parent,"student_email_id"),sub,msg)

def exam_declaration_for_instructor_submit(doc):
    sub = "Exam Declaration for {0}".format(doc.exam_program)
    msg="""<p>--------Exam Details----------</p>"""
    msg="""<p>The exam has been declared for {0}</p>""".format(doc.exam_program)
    msg+="""<p>Exam Declaration Id : {0}</p>""".format(doc.name)
    msg+="""<p>Exam Program : {0}</p>""".format(doc.exam_program)
    msg+="""<p>Exam start date : {0}</p>""".format(doc.exam_start_date)
    msg+="""<p>Exam End Date : {0}</p>""".format(doc.exam_end_date)
    msg+="""<p>Exam Semester:</p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Semester</th>"""
    for d in doc.get("semesters"):
        msg += """<tr><td>{0}</td></tr>""".format(str(d.get('semester'))) 
    msg += "</table>"
    msg+="""<p>Offered Courses Offered : </p>"""
    msg += """</u></b></p><table class='table table-bordered'><tr>
        <th>Courses</th><th>Course Name</th><th>Course Code</th><th>Semester</th><th>Examination Date</th><th>From Time</th><th>To Time</th><th>Total Duration(In Hours)</th>"""
    for d in doc.get("courses_offered"):
        msg += "<tr><td>" + """{0}""".format(str(d.get('courses'))) + "</td><td>" + str(d.get('course_name') or '') + "</td><td>" + str(d.get('course_code')) + "</td><td>" + str(d.get('semester')) + "</td><td>" + str(d.get('examination_date')) + "</td><td>" + str(d.get('from_time')) + "</td><td>" + str(d.get('to_time')) + "</td><td>" + str(d.get('total_duration_in_hours')) +  "</td></tr>"
    msg += "</table>"
    semester_list =[s.semester for s in doc.semesters]
    course_list = [c.courses for c in doc.courses_offered]
    instructor_list = frappe.db.get_all('Instructor Log',{'programs': doc.exam_program, 'program': ('in', semester_list), 'academic_year': doc.academic_year, 'academic_term':doc.academic_term}, 'parent')
    for i in instructor_list:
        instructor_name = frappe.db.get_value('Instructor',{'name':i.get('parent')},'instructor_name')
        send_mail(frappe.db.get_value("User",{'full_name':instructor_name, 'enabled':1},"email"),sub,msg)

def exam_evaluation_plan_for_paper_setter_submit(doc):
    sub = "You are invited to do paper setting for exam declaration {0}".format(doc.exam_declaration)
    msg1="""<p>--------Exam Details----------</p>"""
    msg1+="""<p>Exam Declaration : {0}</p>""".format(doc.exam_declaration)
    msg1+="""<p>Program : {0}</p>""".format(doc.programs)
    msg1+="""<p>Semster :  {0}</p>""".format(doc.program)
    for e in doc.examiners_list:
        msg = ""
        msg+="""<p>Course : {0}</p><p>Course Name:{1}</p><p>Course Code:{2}</p>""".format(e.course,e.course_name,e.course_code)
        msg+="""<p>Assessment Criteria:{0}</p>""".format(doc.assessment_criteria)
        msg+="""<p>Academic Year :{0}</p>""".format(doc.academic_year)
        msg+="""<p>Academic Term:{0}</p>""".format(doc.academic_term)
        msg+="""<p>Paper Setting Start Date:{0}</p>""".format(doc.paper_setting_start_date)
        msg+="""<p>Paper Setting End Date:{0}</p>""".format(doc.paper_setting_end_date)
        employee = frappe.db.get_value('Instructor',{'name':e.paper_setter},'employee')
        email = frappe.db.get_value('Employee',{'name':employee},'user_id')
        if frappe.db.get_value("User",{'email':email, 'enabled':1},"email"):
            send_mail(email,sub,msg1+msg)

def exam_evaluation_plan_for_moderator_submit(doc):
    sub = "You are invited as moderator for exam declaration {0}".format(doc.exam_declaration)
    msg1="""<p>--------Exam Details----------</p>"""
    msg1+="""<p>Exam Declaration : {0}</p>""".format(doc.exam_declaration)
    msg1+="""<p>Program : {0}</p>""".format(doc.programs)
    msg1+="""<p>Semster :  {0}</p>""".format(doc.program)
    for e in doc.moderator_list:
        msg = ""
        msg+="""<p>Course : {0}</p><p>Course Name:{1}</p><p>Course Code:{2}</p>""".format(e.course,e.course_name,e.course_code)
        msg+="""<p>Assessment Criteria:{0}</p>""".format(doc.assessment_criteria)
        msg+="""<p>Academic Year :{0}</p>""".format(doc.academic_year)
        msg+="""<p>Academic Term:{0}</p>""".format(doc.academic_term)
        msg+="""<p>Paper Setting Start Date:{0}</p>""".format(doc.paper_setting_start_date)
        msg+="""<p>Paper Setting End Date:{0}</p>""".format(doc.paper_setting_end_date)
        employee = frappe.db.get_value('Instructor',{'name':e.moderator},'employee')
        email = frappe.db.get_value('Employee',{'name':employee},'user_id')
        if frappe.db.get_value("User",{'email':email, 'enabled':1},"email"):
            send_mail(email,sub,msg1+msg)