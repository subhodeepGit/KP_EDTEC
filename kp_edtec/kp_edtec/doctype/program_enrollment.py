import frappe
from frappe import msgprint, _
from frappe.utils import comma_and, get_link_to_form, getdate,date_diff,add_days
from kp_edtec.kp_edtec.doctype.custom_naming_series  import get_default_naming_series,make_autoname,_field_autoname,set_name_by_naming_series,_prompt_autoname,_format_autoname
from kp_edtec.kp_edtec.utils import get_courses_by_semester,duplicate_row_validation
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions
from kp_edtec.kp_edtec.notification.custom_notification import program_enrollment_admitted,program_enrollment_provisional_admission
from frappe.utils.background_jobs import enqueue
# from frappe.desk.reportview import get_match_cond

def validate(doc,method):
    set_duration(doc)
    get_set_holding_date(doc)
    duplicate_row_validation(doc,"courses",["course"])

    student=frappe.get_doc("Student",doc.student)
    student.roll_no=doc.roll_no
    student.save()

def set_duration(doc):
    for event in doc.academic_events_table:
        event.duration = date_diff(event.end_date , event.start_date)

def on_change(doc,method):
    for course in doc.get("courses"):
        if not course.course_name:
            course.course_name=frappe.db.get_value("Program Course",{"course":course.course},'course_name')

    validate_enrollment_admission_status(doc)
    if doc.docstatus==1:
        if doc.admission_status=="Provisional Admission":
            program_enrollment_provisional_admission(doc)
        else:
            program_enrollment_admitted(doc)
    #     update_enrollment_admission_status(doc)

@frappe.whitelist()
def get_program_enrollment(student):
    data=frappe.get_all("Program Enrollment",{'student':student,'docstatus':1},['name','program','programs'],limit=1)
    if len(data)>0:
        return data[0]


@frappe.whitelist()
def get_roll(student):
        id_student=frappe.get_all("Student",filters=[['name','=',student]],fields=['name','roll_no','permanant_registration_number'])
        return id_student[0]


def on_cancel(doc,method):
    update_reserved_seats(doc)
    delete_permissions(doc)
    # enqueue(delete_permissions, queue='default', timeout=6000, event='delete_permissions',program_enrollment=doc.name)
    delete_course_enrollment(doc)
    # enqueue(delete_course_enrollment, queue='default', timeout=6000, event='delete_course_enrollment',program_enrollment=doc.name)
    update_student(doc)

def on_submit(doc,method):
    make_fee_records(doc)
    # enqueue(create_student, queue='default', timeout=6000, event='create_student',program_enrollment=doc.name)
    # enqueue(make_fee_records, queue='default', timeout=6000, event='make_fee_records',program_enrollment=doc.name)
    create_student(doc)
    update_reserved_seats(doc,on_submit=1)
    update_enrollment_admission_status(doc)
    # update_student_applicant(doc)

def create_student(doc):
    student=frappe.get_doc("Student",doc.student)
    # student.roll_no = doc.roll_no                               #Rupali:01Apr2022
    student.set("current_education",[])
    student.append("current_education",{
            "programs":doc.programs,
            "semesters":doc.program,
            "academic_year":doc.academic_year,
            "academic_term":doc.academic_term           
        })
    if student.student_email_id:
        if not frappe.db.exists("User",student.student_email_id):
            user=frappe.new_doc("User")
            
        else:
            user=frappe.get_doc("User",student.student_email_id)
        set_PRN_number(doc)
        user.email=student.student_email_id
        user.first_name=student.first_name
        user.last_name=student.last_name       
        user.module_profile="Student"
        user.enabled=1
        student.user=student.student_email_id
        user.save()
        set_permission_to_student(user.name,doc)
        add_enrollment_details_in_student(doc,student)
    student.save()
# @frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
# def get_program_courses(doctype, txt, searchfield, start, page_len, filters):
# 	if not filters.get('program'):
# 		frappe.msgprint(_("Please select a Program first."))
# 		return []

# 	return frappe.db.sql("""select course, course_name, course_code from `tabProgram Course`
# 		where  parent = %(program)s and course like %(txt)s {match_cond}
# 		order by
# 			if(locate(%(_txt)s, course), locate(%(_txt)s, course), 99999),
# 			idx desc,
# 			`tabProgram Course`.course asc
# 		limit {start}, {page_len}""".format(
# 			match_cond=get_match_cond(doctype),
# 			start=start,
# 			page_len=page_len), {
# 				"txt": "%{0}%".format(txt),
# 				"_txt": txt.replace('%', ''),
# 				"program": filters['program']
# 			})
def make_fee_records(doc):
    if doc.reference_doctype=="Student Applicant":
        from erpnext.education.api import get_fee_components
        fee_list = []
        for d in doc.fee_structure_item:
            fee_components = get_fee_components(d.fee_structure)
            if fee_components:
                fees = frappe.new_doc("Fees")
                fees.update({
                    "student": doc.student,
                    "academic_year": doc.academic_year,
                    "academic_term": doc.academic_term,
                    "fee_structure": d.fee_structure,
                    "program": doc.program,
                    "programs": doc.programs,
                    "due_date": d.due_date,
                    "student_name": doc.student_name,
                    "program_enrollment": doc.name,
                    "components": fee_components
                })
                for fsi in frappe.get_all("Fee Structure Item",{"parent":d.name,"student_category":doc.student_category},["fee_structure","due_date"]):
                    fees.due_date=fsi.due_date
                fees.save()
                fees.submit()
                fee_list.append(fees.name)
        if fee_list:
            fee_list = ["""<a href="/app/Form/Fees/%s" target="_blank">%s</a>""" % \
                (fee, fee) for fee in fee_list]
            msgprint(_("Fee Records Created - {0}").format(comma_and(fee_list)))

def set_permission_to_student(user,program_enroll):
    add_user_permission("Student",program_enroll.student, user,program_enroll)
    add_user_permission("Programs",program_enroll.programs, user,program_enroll)
    for inst_log in frappe.get_all("Instructor Log",{"programs":program_enroll.programs,"program":program_enroll.program,"academic_year":program_enroll.academic_year,"academic_term":program_enroll.academic_term},['parent'],group_by="parent"):
        instructor=frappe.get_doc("Instructor",inst_log.parent)
        instructor.save()
            
    if program_enroll.reference_doctype and program_enroll.reference_name:
        add_user_permission(program_enroll.reference_doctype,program_enroll.reference_name, user,program_enroll)
        

@frappe.whitelist()
def get_courses(doctype, txt, searchfield, start, page_len, filters):
    courses=get_courses_by_semester(filters.get("semester"))
    if courses:
        return frappe.db.sql("""select name,course_name,course_code from tabCourse
			where name in ({0}) and (name LIKE %s or course_name LIKE %s or course_code LIKE %s)
			limit %s, %s""".format(", ".join(['%s']*len(courses))),
			tuple(courses + ["%%%s%%" % txt, "%%%s%%" % txt,"%%%s%%" % txt, start, page_len]))
    return []

@frappe.whitelist()
def get_programs(doctype, txt, searchfield, start, page_len, filters):
    fltr = {}
    lst = []
    if txt:
        fltr.update({"programs_":txt})
    for i in frappe.get_all("Student",{'name':filters.get("student")},['student_applicant']):
        for j in frappe.get_all("Student Applicant",{"name":i.get("student_applicant"),"docstatus":1},['programs_']):
            if j.programs_ not in lst:
                lst.append(j.programs_)
    return [(d,) for d in lst]


@frappe.whitelist()
def get_sem(doctype, txt, searchfield, start, page_len, filters):
    fltr = {}
    lst = []
    if txt:
        fltr.update({"program":txt})
    for i in frappe.get_all("Student",{'name':filters.get("student")},['student_applicant']):
        for j in frappe.get_all("Student Applicant",{"name":i.get("student_applicant"),"docstatus":1},['program']):
            if j.program not in lst:
                lst.append(j.program)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_cat(doctype, txt, searchfield, start, page_len, filters):
    fltr = {}
    lst = []
    if txt:
        fltr.update({"student_category":txt})
    for i in frappe.get_all("Student",{'name':filters.get("student")},['student_applicant']):
        for j in frappe.get_all("Student Applicant",{"name":i.get("student_applicant"),"docstatus":1},['student_category']):
            if j.student_category not in lst:
                lst.append(j.student_category)
    return [(d,) for d in lst]


@frappe.whitelist()
def get_term(doctype, txt, searchfield, start, page_len, filters):
    fltr = {}
    lst = []
    if txt:
        fltr.update({"academic_term":txt})
    for i in frappe.get_all("Student",{'name':filters.get("student")},['student_applicant']):
        for j in frappe.get_all("Student Applicant",{"name":i.get("student_applicant"),"docstatus":1},['academic_term']):
            if j.academic_term not in lst:
                lst.append(j.academic_term)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_year(doctype, txt, searchfield, start, page_len, filters):
    fltr = {}
    lst = []
    if txt:
        fltr.update({"academic_year":txt})
    for i in frappe.get_all("Student",{'name':filters.get("student")},['student_applicant']):
        for j in frappe.get_all("Student Applicant",{"name":i.get("student_applicant"),"docstatus":1},['academic_year']):
            if j.academic_year not in lst:
                lst.append(j.academic_year)
    return [(d,) for d in lst]

def add_enrollment_details_in_student(doc,student):
    if doc.reference_doctype in ["Student Applicant","Student Exchange Applicant"] and doc.reference_name:
        applicant=frappe.get_doc(doc.reference_doctype,doc.reference_name)
        student.set("education_details",[])
        for app in applicant.get("education_qualifications_details"):
            student.append("education_details",{
                "qualification":app.qualification,
                "institute":app.institute,
                "board":app.board,
                "percentage":app.percentage_cgpa,
                "score":app.score,
                "year_of_completion":app.year_of_completion
            })

        if doc.reference_doctype=="Student Applicant":
            student.physically_disabled = doc.physically_disabled
            student.set("disable_type",[])
            for d in doc.get("disable_type"):
                student.append("disable_type",{
                    "disability_type":d.disability_type,
                    "percentage_of_disability":d.percentage_of_disability
                })

            student.award_winner = doc.award_winner
            student.set("awards_list",[])
            for d in doc.get("awards_list"):
                student.append("awards_list",{
                    "awards":d.awards,
                    "won_in_year":d.won_in_year
                })
    if doc.permanant_registration_number:
        student.permanant_registration_number=doc.permanant_registration_number

@frappe.whitelist()
def get_academic_calender_table(programs,semester):
    for d in frappe.get_all("Academic Calendar Template",{"programs":programs,"program":semester}):
        doc=frappe.get_doc("Academic Calendar Template",d.name)
        table=[]
        for d in doc.get("academic_events_table"):
            table.append({
                "academic_events":d.academic_events,
                "start_date":d.start_date,
                "end_date":d.end_date,
                "duration":d.duration
            }
            )
        return table

@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                                Select 
                                        distinct(st.name) as student, st.title as student_name ,st.roll_no as roll_no,st.permanant_registration_number as permanant_registration_number
                                from `tabCurrent Educational Details` ced 
                                left join `tabStudent` st on st.name=ced.parent 
                                where enabled=1 and (st.name LIKE %(txt)s or st.title LIKE %(txt)s) and ced.programs='{0}'""".format(filters.get("programs")),dict(txt="%{}%".format(txt)))    
def set_PRN_number(doc):
    if not frappe.db.get_value("Student",doc.student,"permanant_registration_number"):
        autoname=frappe.db.get_single_value("Educations Configurations","student_registration_naming")

        # if not autoname:
            # frappe.throw("set <b>Student Registration Naming</b> In <b>Educations Configurations</b> for <b>Permanant Registration Number</b>")
        _autoname = autoname.lower()

        if _autoname.startswith("field:"):
            doc.permanant_registration_number = _field_autoname(autoname, doc)
        elif _autoname.startswith("naming_series:"):
            set_name_by_naming_series(doc,autoname)
        elif _autoname.startswith("prompt"):
            _prompt_autoname(autoname, doc)
        elif _autoname.startswith("format:"):
            doc.permanant_registration_number = _format_autoname(autoname, doc)
        elif "#" in autoname:
            doc.permanant_registration_number = make_autoname(autoname, doc=doc)
        doc.save()

def set_name_by_naming_series(doc,autoname):
    """Sets name by the `naming_series` property"""

    doc.permanant_registration_number = make_autoname(autoname+".#####", "", doc)
    

@frappe.whitelist()
def get_seat_reservation_type(doctype, txt, searchfield, start, page_len, filters):
    reservation_type=[]
    for i in frappe.get_all("Student Applicant",{"name":filters.get("student_applicant"),"docstatus":1},['student_admission','physically_disabled','award_winner']):
        for d in frappe.get_all("Reservations List",{"parent":i.get("student_admission"),'seat_reservation_type': ['like', '%{}%'.format(txt)]},['seat_reservation_type']):
            if d.seat_reservation_type=="Physically Disabled":
                if i.physically_disabled:
                    reservation_type.append((d.seat_reservation_type,))
            elif d.seat_reservation_type=="Sport Person":
                if i.award_winner:
                    reservation_type.append((d.seat_reservation_type,))
            else:
                reservation_type.append((d.seat_reservation_type,))
    return reservation_type

@frappe.whitelist()
def get_programs_stud_app(doctype, txt, searchfield, start, page_len, filters):
    fltr = {"parent":filters.get("student_applicant")}
    if txt:
        fltr.update({'semester': ['like', '%{}%'.format(txt)]})
    return frappe.get_all("Program Priority",fltr,['programs'], as_list=1)

@frappe.whitelist()
def get_program_stud_app(doctype, txt, searchfield, start, page_len, filters):
    fltr = {"programs":filters.get("programs"),"parent":filters.get("student_applicant")}
    if txt:
        fltr.update({'semester': ['like', '%{}%'.format(txt)]})
    return frappe.get_all("Program Priority",fltr,['semester'], as_list=1)

@frappe.whitelist()
def get_data_stud_app(student_applicant):
    return frappe.get_all("Program Priority",{"parent":student_applicant},['programs', 'semester'])


def update_reserved_seats(doc,on_submit=0):
    if doc.reference_doctype and doc.reference_name and doc.reference_doctype in ["Student Applicant","Branch Sliding Application"]:

        # for applicant
        if doc.reference_doctype == "Student Applicant":
            
            for ad in frappe.get_all("Program Priority",{"parent":doc.reference_name,"programs":doc.programs,"semester":doc.program},["student_admission"]):
                admission=frappe.get_doc("Student Admission",ad.student_admission)

                # check reservation type exists
                if len(frappe.get_all("Reservations List",{"seat_reservation_type":doc.seat_reservation_type,"parent":admission.name}))==0:
                    frappe.throw("Reservation Type <b>{0}</b> Not Exists in Admission <b>{1}</b>".format(doc.seat_reservation_type,admission.name))

                # check checkbox values
                for reservation_type in frappe.get_all("Seat Reservation Type",{"name":doc.seat_reservation_type},["physically_disabled","award_winner","name"]):
                    
                    if doc.physically_disabled != reservation_type.physically_disabled:
                        frappe.throw("Please Mark Checkbox <b>{0}</b> for Reservation Type <b>{1}</b>".format("Physically Disabled",doc.seat_reservation_type)) 

                    if doc.award_winner != reservation_type.award_winner:
                        frappe.throw("Please Mark Checkbox <b>{0}</b> for Reservation Type <b>{1}</b>".format("Award Winner",doc.seat_reservation_type))

                    validate_reservation_type_by_criteria(doc,reservation_type.name)

                # update seat 
                for d in admission.get("reservations_distribution"):
                    if doc.seat_reservation_type==d.seat_reservation_type:
                        if on_submit:
                            d.seat_balance-=1
                        else:
                            d.seat_balance+=1
                admission.save()
        
        # branch sliding
        else:
            for application in frappe.get_all("Branch Sliding Application",{"name":doc.reference_name},['branch_sliding_declaration','sliding_in_program']):
                if application.branch_sliding_declaration:
                    declaration=frappe.get_doc("Branch sliding Declaration",application.branch_sliding_declaration)

                    for criteria in declaration.get("branch_sliding__criteria"):
                        if criteria.program==application.sliding_in_program:
                            if on_submit:
                                criteria.available_seats-=1
                            else:
                                criteria.available_seats+=1
                                
                    declaration.validate_seats()
                    declaration.submit()


def validate_reservation_type_by_criteria(doc,reservation_type):
    
    # if criteria not match
    not_exist_in_criteria=True
    
    for d in frappe.get_all("Seat Reservations category Item",{"parent":reservation_type},['for_criteria','allowed_for']):
        fieldname,label=get_field_name(doc,d.for_criteria)
        if not doc.get(fieldname):
            frappe.throw("Please Select <b>{0}</b> for this <b>Reservation Type</b>".format(label))
        if label==d.for_criteria:
            not_exist_in_criteria=False
        
    if not_exist_in_criteria:
        frappe.throw("Candidate not fits for this Criteria <b>{0}</b> ".format(reservation_type))
                
def get_field_name(doc,linked_field):
    for f in frappe.get_meta(doc.doctype).fields: 
        if f.fieldtype=="Link" and f.options==linked_field:
            return f.fieldname,f.label
    frappe.throw("Link Field <b>{0}</b> Not Exist In <b>{1}</b>".format(linked_field,doc.doctype))


def update_student_applicant(doc):
    if doc.reference_doctype == "Student Applicant":
        student_applicant=frappe.get_doc("Student Applicant",doc.reference_name)
        student_applicant.application_status="Admitted"
        # student_applicant.physically_disabled = doc.physically_disabled
        # for d in doc.get("disable_type"):
        #     student_applicant.append("disable_type",{
        #         "disability_type":d.disability_type,
        #         "percentage_of_disability":d.percentage_of_disability
        #     })

        # student_applicant.award_winner = doc.award_winner
        
        # for d in doc.get("awards_list"):
        #     student_applicant.append("awards_list",{
        #         "awards":d.awards,
        #         "won_in_year":d.won_in_year
        #     })

        student_applicant.submit()

def get_set_holding_date(doc):
    if doc.is_provisional_admission=="Yes" and doc.reference_doctype=="Student Applicant":
        for priority in frappe.get_all("Program Priority",{"programs":doc.programs,"semester":doc.program},['student_admission']):
            duration=frappe.db.get_value("Student Admission",{"name":priority.student_admission},'seat_holding_duration')
            if duration:
                doc.seat_holding_till=add_days(doc.enrollment_date,duration)

def update_enrollment_admission_status(doc):
    if doc.is_provisional_admission=="Yes":
        doc.admission_status="Provisional Admission"
    else:
        doc.admission_status="Admitted"

@frappe.whitelist()
def get_available_seats(student_applicant, seat_reservation_type,programs,program):
    if student_applicant and seat_reservation_type :  
        for priority in frappe.get_all("Program Priority",{"programs":programs,"semester":program, "parent":student_applicant},['student_admission']):
            seat_balance=frappe.db.get_value("Reservations List",{"parent":priority.student_admission, 'seat_reservation_type':seat_reservation_type},'seat_balance')
            if seat_balance:
                return seat_balance

def delete_course_enrollment(doc):
    for ce in frappe.get_all("Course Enrollment",{"program_enrollment":doc.name}):
        frappe.delete_doc("Course Enrollment",ce.name)

def delete_permissions(doc):
    # for cr_enroll in frappe.get_all("Course Enrollment",{"program_enrollment":doc.name}):
    #     for usr in frappe.get_all("User Permission",{"allow":"Course Enrollment","for_value":cr_enroll.name}):
    #         frappe.delete_doc("User Permission",usr.name)
    # for cr_enroll in frappe.get_all("Course Enrollment",{"program_enrollment":doc.name}):
    #     for usr in frappe.get_all("User Permission",{"reference_doctype":"Course Enrollment","reference_docname":cr_enroll.name}):
    #         frappe.delete_doc("User Permission",usr.name)       
    delete_ref_doctype_permissions(["Programs","Course Enrollment","Course"],doc)


def validate_enrollment_admission_status(doc):
    if doc.is_provisional_admission=="Yes" and doc.admission_status!="Provisional Admission":
        frappe.throw("If you select Is Provisional Admission <b>Yes</b> Then Admission Status should be <b>Provisional Admission</b>")

    elif (doc.is_provisional_admission=="No" and doc.admission_status and doc.admission_status=="Provisional Admission"):
        frappe.throw("If you select Is Provisional Admission <b>No</b> Then Admission Status should not be <b>Provisional Admission</b>") 


def update_student(doc):
    student=frappe.get_doc("Student",doc.student)
    student.set("current_education",[])
    for enroll in frappe.get_all("Program Enrollment",{"docstatus":1,"student":doc.student},limit=1):
        student.append("current_education",{
            "programs":doc.programs,
            "semesters":doc.program,
            "academic_year":doc.academic_year,
            "academic_term":doc.academic_term
        })
    student.save()