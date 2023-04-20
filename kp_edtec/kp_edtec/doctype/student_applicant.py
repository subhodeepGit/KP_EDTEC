import frappe,json,re
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _
from kp_edtec.kp_edtec.utils import duplicate_row_validation
# from kp_edtec.kp_edtec.notification.custom_notification import student_applicant_submit


def validate(doc,method):
    # validate_percentage(doc)
    education_details_validation(doc)
    document_list_checkbox(doc)
    mobile_number_validation(doc)
    validate_pin_code(doc)
    update_education_parameters(doc)
    duplicate_row_validation(doc,"program_priority",["programs"])
    validate_seat_reservation_type(doc)
    if len(doc.document_list ) == 0:
        add_document_list_rows(doc)
    get_admission_fees(doc)
    mobile_number_validation(doc)
    email_validation(doc)
    isValidPinCode(doc.pin_code)
    get_phone_code(doc)
    if len(doc.program_priority ) == 0:
        set_web_form_fields(doc)

# def on_submit(self):
#     student_applicant_submit(self)
def document_list_checkbox(doc):
    for d in doc.get("document_list"):
        if d.attach!=None:
            d.attached=1

        else:
            d.attached=0

            # frappe.db.set_value("Document List",self.name,'attached',1)
            


def mobile_number_validation(doc):
    
    if doc.local_guardian_contact_no:
       
        if not (doc.local_guardian_contact_no).isdigit():
            frappe.throw("Field <b>Local Guardian Contact Number</b> Accept Digits Only")
        if len(doc.local_guardian_contact_no)<10:
            frappe.throw("Field <b>Local Guardian Contact Number</b> must be 10 Digits")
        if len(doc.local_guardian_contact_no)>10:
            frappe.throw("Field <b>Local Guardian Contact Number</b> must be 10 Digits")


    if doc.fathers_contact_number:
        
        if not (doc.fathers_contact_number).isdigit():
            frappe.throw("Field <b>Father's Contact Number</b> Accept Digits Only")
        if len(doc.fathers_contact_number)<10:
            frappe.throw("Field <b>Father's Contact Number</b> must be 10 Digits")
        if len(doc.fathers_contact_number)>10:
            frappe.throw("Field <b>Father's Contact Number</b> must be 10 Digits")

    if doc.fathers_contact_number:
        
        if not (doc.mothers_contact_number).isdigit():
            frappe.throw("Field <b>Mother's Contact Number</b> Accept Digits Only")
        if len(doc.mothers_contact_number)<10:
            frappe.throw("Field <b>Mother's Contact Number</b> must be 10 Digits")
        if len(doc.mothers_contact_number)>10:
            frappe.throw("Field <b>Mother's Contact Number</b> must be 10 Digits")

def validate_pin_code(doc):
    
    # try:
    if doc.pin_code:

        if len(doc.pin_code)<6:
            frappe.throw("Field <b>Pincode</b> must be 6 Digits")
        if len(doc.pin_code)>6:
            frappe.throw("Field <b>Pincode</b> must be 6 Digits")
def set_web_form_fields(doc):
    prgram_list = [doc.program_choice_1, doc.program_choice_2,doc.program_choice3, doc.program_choice_4, doc.program_choice_5, doc.program_choice_6 ]
    if len(prgram_list) > 0:
        doc.set("program_priority",[])
        for pro in prgram_list:
            program_data = get_admission_and_semester_by_program(pro,doc.program_grade,doc.academic_year)
            doc.append("program_priority",{
                "programs":pro,
                "semester": program_data.get('semester'),
                "student_admission":program_data.get('name')
            }) 

       
    for i in doc.education_qualifications_details:
        i.qualification = i.qualification_ if i.qualification_ else i.qualification
        i.year_of_completion = i.year_of_completion_ if i.year_of_completion_ else i.year_of_completion
        i.qualification_ = i.qualification if i.qualification else i.qualification_
        i.year_of_completion_ = i.year_of_completion if i.year_of_completion else i.year_of_completion_
    for j in doc.document_list:
        j.document_name = j.document_name_ if j.document_name_ else j.document_name
        j.document_name_ = j.document_name if j.document_name else j.document_name_

def validate_percentage(doc):
    for eqd in doc.get('education_qualifications_details'):
        parameter_list = frappe.get_all("Eligibility Parameter List",{"parent":doc.counselling_structure}, ['parameter', 'eligible_score'])
        for p in parameter_list:
            if eqd.qualification == p.parameter:
                if eqd.score and eqd.score < p.eligible_score:
                    frappe.throw("You are not eligible for qualification <b>{0}</b>.".format(eqd.qualification))
        if eqd.percentage_cgpa:
            for program in doc.program_priority:
                percent_cgpa= [ i['percentagecgpa'] for i in frappe.get_all("Eligibility Parameter List",{"parent":program.student_admission,"student_category":doc.student_category, "parameter":eqd.qualification},'percentagecgpa' )]
                if percent_cgpa and  eqd.percentage_cgpa != percent_cgpa[0]:
                    frappe.throw("Please correct option for Percentage/CGPA for row no .<b>{0}</b> in Education Qualifications Details.".format(eqd.idx))

def on_update(doc,method):
    if doc.docstatus==1:
        validate_attachment(doc)
    if doc.application_status=="Approved" and doc.docstatus==1:
        student = get_mapped_doc("Student Applicant", doc.name,
            {
            "Student Applicant": {
                "doctype": "Student",
                "field_map": {
                    "name": "student_applicant"
                }
            },
            "Education Qualifications Details": {
                "doctype": "Educational Details"
            },
            "Document List": {
                "doctype": "Document List"
            }
        }, ignore_permissions=True)
        student.save()
        if doc.account_name and doc.bank and doc.account_type and doc.branch_code and doc.bank_account_no:
            acc_doc = frappe.new_doc('Bank Account')
            acc_doc.account_name = doc.account_name
            acc_doc.bank =  doc.bank
            acc_doc.account_type =  doc.account_type
            acc_doc.branch_code =  doc.branch_code
            acc_doc.bank_account_no =  doc.bank_account_no
            acc_doc.party_type = "Student"
            acc_doc.party = frappe.db.get_value("Student", {'student_applicant': doc.name},'name')
            acc_doc.save()
            frappe.msgprint(_("Bank account created"))
    
def education_details_validation(doc):
    if doc.student_category and doc.student_admission:
        for d in get_eligibility_parameter_list_for_category(doc.student_admission,doc.student_category):
            if d.parameter not in [ed.qualification for ed in doc.get("education_qualifications_details")]:
                frappe.throw("Please Add <b>{0}</b> in Education Details Table".format(d.parameter))
           
def mobile_number_validation(doc):
    if doc.student_mobile_number:
        if not (doc.student_mobile_number).isdigit():
            frappe.throw("Field <b>Mobile Number</b> Accept Digits Only")
        if len(doc.student_mobile_number)>10:
            frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")
        if len(doc.student_mobile_number)<10:
            frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")

def email_validation(doc):
    for stu_app in frappe.get_all("Student Applicant",{"student_email_id":doc.student_email_id,"docstatus":("!=",2),"name":("!=",doc.name)}):
        frappe.throw("<b>Email ID</b> already Exist <b><a href='/app/student-applicant/{0}' target='_blank'>{0}</a></b>".format(stu_app.name))

def add_document_list_rows(doc): 
    if doc.student_category and doc.academic_year:
        doc.set("document_list",[])
        for d in get_document_list_by_category(doc):
            doc.append("document_list",{
                "document_name":d.document_name,
                "mandatory":d.mandatory,
                "is_available" :d.is_available
            })

def status_validation(doc):
    if doc.student_admission and doc.application_status=="Approved":
        admission_doc=frappe.get_doc("Student Admission",doc.student_admission)
        if admission_doc.counselling_fees=="YES":
            for st in frappe.get_all("Student",{"student_applicant":doc.name}):
                if len(frappe.get_all("Fees",{"student":st.name}))<1:
                    frappe.throw("Please Pay Fess First")
        
def get_year_list(from_year,to_year):
    year_list=[]
    if from_year == to_year:
        year_list.append(from_year)
    else:
        if '-' in from_year and '-' in to_year:
            new_from_year=from_year
            year_list.append(from_year)
            while new_from_year != to_year:
                new_from_year=str(int(new_from_year.split('-')[0])+1)+"-"+str(int(new_from_year.split('-')[1])+1)
                year_list.append(new_from_year)
    return year_list

def update_education_parameters(doc):
    if doc.program_priority:
        main_result = ""
        for program in doc.program_priority:
            parameters= frappe.get_all("Eligibility Parameter List",{"parent":program.student_admission,"student_category":doc.student_category},['parameter', 'percentagecgpa', 'total_score', 'eligible_score'],order_by="idx")
            edu_detail ="<b> * "+ program.student_admission+"</b><br>"
            str_data = ""
            for p in parameters[0:]:
                str_p = str(parameters.index(p)+1)+"] Parameter:"
                if p['parameter']:
                    str_p = str_p+ p['parameter'] +", "
                str_p= str_p+ " Percent/CGPA:"
                if p['percentagecgpa']:
                    str_p = str_p + p['percentagecgpa']+", "
                str_p= str_p+" Eligible Score:"
                if p['eligible_score']:
                    str_p = str_p +str(p['eligible_score'])+", "
                str_p = str_p+" Total Score:"
                if p['total_score']:
                    str_p = str_p + str(p['total_score'])+"<br>"
                str_data = str_data + str_p
            edu_detail = edu_detail + str_data
            main_result = main_result+edu_detail+"<br>"
        doc.education_detail = main_result

def get_admission_fees(doc):
   doc.set("admission_fees",[])
   for admission in doc.get('program_priority'):
       doc.append("admission_fees",{
           "admission":admission.student_admission,
           "programs":admission.programs,
           "fees":get_fees_by_category(doc,admission.student_admission) or 0
       })
def get_fees_by_category(doc,admission):
    student_admission=frappe.get_doc("Student Admission",admission)
    if student_admission.admission_fees=="YES":
        for d in student_admission.get("admission_fee_structure"):
            if d.student_category==doc.student_category:
                return d.amount
@frappe.whitelist()
def get_student_applicant_details(student):
    for st in frappe.get_all("Student",{'name':student},['student_applicant']):
        if st.get('student_applicant'):
            for st_app in frappe.get_all("Student Applicant",{"name":st.get('student_applicant'),"docstatus":1}):
                return frappe.get_doc("Student Applicant",st_app)

@frappe.whitelist()
def get_eligibility_parameter_list_for_category(admission,category):
    parameter_list = frappe.get_all("Eligibility Parameter List",{"parent":admission,"student_category":category},['parameter'],order_by="parameter_name asc")
    return parameter_list

def get_document_list_by_category(doc):
    filters={"student_category":doc.student_category}
    group_by=""
    if doc.counselling_structure:
        filters.update({"parent":doc.counselling_structure,"parenttype":"Counselling Structure"})
    else:
        filters.update({"parent":["IN",[d.student_admission for d in doc.get('program_priority')]],"parenttype":"Student Admission"})
        group_by="document_name"
    doc_list  = frappe.db.sql("""SELECT DL.document_name, DL.mandatory, DL.is_available from `tabDocuments Template List` as DL 
    inner join `tabDocuments Template` as D on DL.parent= D.name where D.student_category='{0}' and D.academic_year = '{1}'""".format(doc.student_category,doc.academic_year), as_dict=1)
    return doc_list if doc_list else []
# def on_submit(self):
#         student_applicant_submit(self)
@frappe.whitelist()
def enroll_student(source_name):
    from kp_edtec.kp_edtec.doctype.student_exchange_applicant.student_exchange_applicant import get_academic_calender_table
    from kp_edtec.kp_edtec.doctype.semesters.semesters import get_courses
    st_applicant=frappe.get_doc("Student Applicant", source_name)
    for student in frappe.get_all("Student",{"student_applicant":source_name},['name','student_category','title']):
        program_enrollment = frappe.new_doc("Program Enrollment")
        program_enrollment.student = student.name
        program_enrollment.student_category = student.student_category
        program_enrollment.student_name = student.title
        program_enrollment.roll_no = student.roll_no
        program_enrollment.programs = st_applicant.programs_
        program_enrollment.program = st_applicant.program
        program_enrollment.academic_year=st_applicant.academic_year
        program_enrollment.academic_term=st_applicant.academic_term
        program_enrollment.reference_doctype="Student Applicant"
        program_enrollment.reference_name=source_name
        program_enrollment.program_grade = st_applicant.program_grade
        program_enrollment.gender=st_applicant.gender
        program_enrollment.physically_disabled=st_applicant.physically_disabled
        program_enrollment.award_winner=st_applicant.award_winner
        program_enrollment.boarding_student=st_applicant.hostel_required
        
        for d in st_applicant.get("disable_type"):
            program_enrollment.append("disable_type",{
                "disability_type":d.disability_type,
                "percentage_of_disability":d.percentage_of_disability
            })
        
        for d in st_applicant.get("awards_list"):
            program_enrollment.append("awards_list",{
                "awards":d.awards,
                "won_in_year":d.won_in_year
            })

        if st_applicant.program:
            for crs in get_courses(st_applicant.program):
                program_enrollment.append("courses",crs)
        if st_applicant.student_admission:
            st_admission=frappe.get_doc("Student Admission",st_applicant.student_admission)
            if st_admission.admission_fees=="YES":
                for fs in st_admission.get("admission_fee_structure"):
                    if fs.student_category==student.student_category:
                        program_enrollment.append("fee_structure_item",{
                            "student_category":student.student_category,
                            "fee_structure":fs.fee_structure,
                            "amount":fs.amount,
                            "due_date":fs.due_date
                        })
                    
            if st_admission.academic_calendar:
                for d in get_academic_calender_table(st_admission.academic_calendar):
                    program_enrollment.append("academic_events_table",d)
        return program_enrollment
        
@frappe.whitelist()
def show_fees_button(student_applicant,student_admission):
    if student_admission:
        admission_doc=frappe.get_doc("Student Admission",student_admission)
        if admission_doc.counselling_fees=="YES":
            for st in frappe.get_all("Student",{"student_applicant":student_applicant}):
                if len(frappe.get_all("Fees",{"student":st.name,"docstatus":1}))>0:
                    return False
        else:
            return False
    return True

@frappe.whitelist()
def create_fees(source_name, target_doc=None):
    from kp_edtec.kp_edtec.doctype.program_enrollment import get_program_enrollment
    from erpnext.education.api import get_fee_components

    def set_missing_values(source, target):
        for d in frappe.get_all("Counselling Structure",{"name":source.counselling_structure}):
            for fsi in frappe.get_all("Fee Structure Item",{"parent":d.name,"parentfield":"counselling_fees","student_category":source.student_category},["fee_structure","due_date"]):
                target.fee_structure=fsi.fee_structure
                target.due_date=fsi.due_date
        if target.fee_structure:
            fee_components = get_fee_components(target.fee_structure)
            target.update({"components": fee_components})
        if source.student_email_id:
            student = frappe.db.get_value("Student", {'student_email_id':source.student_email_id}, 'name')
            target.student = student

        target.programs=''
        target.program=''
        if get_program_enrollment(target.student):
            target.program_enrollment=get_program_enrollment(target.student)['name']
            target.programs=get_program_enrollment(target.student)['programs']
            target.program=get_program_enrollment(target.student)['program']
            target.has_program_enrollment=1

    doclist = get_mapped_doc("Student Applicant", source_name,  {
        "Student Applicant": {
            "doctype": "Fees",
            "validation": {
                "docstatus": ["=", 1]
            },
            "field_map":{
                "doctype":"reference_doctype",
                "name":"reference_docname"
            }
        },
    }, target_doc,set_missing_values)
    return doclist


def validate_attachment(doc):
    for d in doc.get("document_list"):
        if d.mandatory and not d.attach:
            frappe.throw("Please Attach Document <b>{0}</b>".format(d.document_name))


def validate_student_admission(doc):
    for i in doc.program_priority:
        stud_admi_data = frappe.db.sql("""SELECT CA.student_admission, CS.name from `tabProgram Priority` as CA inner join `tabStudent Applicant`  as CS on CA.parent = CS.name where CS.academic_year = '{0}' and CS.docstatus=1""".format(doc.academic_year), as_dict=1)
        if i.student_admission in [d.student_admission for d in stud_admi_data]:
            exist_data = ', '.join(map(str, [d.name for d in stud_admi_data]))
            frappe.throw("Student admission <b>'{0}'</b> already exists in Counselling Structure <b>'{1}'</b> ".format(i.student_admission, exist_data))

@frappe.whitelist()
def get_document_list(student_category):
    doc_list  = frappe.db.sql("""SELECT DL.document_name, DL.mandatory, DL.is_available from `tabDocuments Template List` as DL 
    inner join `tabDocuments Template` as D on DL.parent= D.name where D.student_category='{0}'""".format(student_category), as_dict=1)
    return doc_list

@frappe.whitelist()
def get_sharing_type():
    capacity=""
    for room in frappe.get_all("Room Type",order_by="capacity",group_by="capacity",fields=["capacity"]):
        capacity+=("\n"+str(room.capacity))

    if not capacity:
        capacity="\n1\n2\n3\n4"

    return capacity

def validate_seat_reservation_type(doc):
    seat_reservation_type_list = [s.seat_reservation_type for s in frappe.get_all("Reservations List",{"parent":["IN",[d.student_admission for d in doc.get("program_priority")]]}, 'seat_reservation_type')]
    if seat_reservation_type_list:
        if doc.physically_disabled:
            physically_disabled_list = [r.name for r in frappe.get_all("Seat Reservation Type",{"name":["IN",seat_reservation_type_list], 'physically_disabled':1}, 'name')]
            if len(physically_disabled_list) == 0 :
                frappe.throw("Seat Reservation Type <b>Physically Disabled</b> Not Exists in Student Admissions List")
        if doc.award_winner:
            award_winner_list = [r.name for r in frappe.get_all("Seat Reservation Type",{"name":["IN",seat_reservation_type_list], 'award_winner':1}, 'name')]
            if len(award_winner_list) == 0 :
                frappe.throw("Seat Reservation Type <b>Award Winner</b> Not Exists in Student Admissions List")

@ frappe.whitelist()
def get_admission_and_semester_by_program(programs,program_grade,academic_year):
    for d in frappe.get_all("Student Admission",{"admission_program":programs,"program_grade":program_grade,"academic_year":academic_year},['name','admission_program','semester','counselling_required','counselling_structure']):
        return d
    return {"no_record_found":1}

@frappe.whitelist()
def get_counselling_structure(program_grade,department,academic_year):
    for d in frappe.get_all("Counselling Structure",{"program_grade":program_grade,"department":department,"academic_year":academic_year}):
        return d

@frappe.whitelist()
def get_education_qualifications_details_by_admissions(student_category,admission):
    return frappe.get_all("Eligibility Parameter List",{"parent":["IN",[d.get("student_admission") for d in json.loads(admission)]],"parenttype":"Student Admission"},["parameter","percentagecgpa"] , order_by="parameter",group_by="parameter")

@frappe.whitelist()
def filter_programs_by_department(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Programs",{"name":['like', '%{}%'.format(txt)],"department":["IN",[d.name for d in frappe.get_all("Department",{"parent_department":filters.get("department")})]],"program_grade":["IN",[d.name for d in frappe.get_all("Program Grades",{"grade":filters.get("program_grade")})]]},as_list=1)

@frappe.whitelist()
def get_qualification_list():
    quali_list =  [q.name for q in frappe.db.get_list("Eligibility Parameters", "name", order_by="parameter_name asc")]
    academic_yr_list =  [q.name for q in frappe.db.get_list("Academic Year", "name", order_by="name")]
    return {'qual':quali_list, 'acadmic':academic_yr_list}

def isValidPinCode(pinCode):
    if pinCode:
    	regex = "^[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}$"

    	p = re.compile(regex)
    	

    	if (pinCode == ''):
    		return False
    		
    	m = re.match(p, pinCode)
    	
    	if m is None:
    		return False
    	else:
    		return True

def get_phone_code(doc):
    if doc.country_code:
        for st in frappe.get_all("State",{"name":doc.states},['country']):
            for cnt in frappe.get_all("Country",{"name":st.country},['country_phone_code']):
                doc.country_code=cnt.country_phone_code

# def update_available_seats(doc):
#     if doc.reference_doctype=="Student Applicant":
#         student_admission = frappe.db.get_value("Student Applicant",{"name":doc.reference_name, 'docstatus':1}, 'student_admission')
#         for sa in frappe.get_all("Student Admission",{"name":student_admission}):
#             sa_doc=frappe.get_doc("Student Admission",sa.name)
#             if len(sa_doc.get('seat_balances')) == 0:
#                 for seat_rd in sa_doc.get("reservations_distribution"):
#                     row = sa_doc.append('seat_balances', {})
#                     row.seat_reservation_type = seat_rd.seat_reservation_type
#                     row.seat = seat_rd.seat
#             sa_doc.save()
#             for seats in sa_doc.get("seat_balances"):
#                 if seats.seat_reservation_type == doc.seat_reservation_type:
#                     seats.seat -= 1
#                 if seats.seat_reservation_type==doc.seat_reservation_type:
#                     if seats.seat==0:
#                         frappe.throw("Seats Not Available For This Student Category <b>{0}</b> in Admission <b>{1}</b>".format(seats.student_category,sa.name))
#             sa_doc.save()
#         #physicaly handicapped
#         # frappe.db.get_value("Student Applicant",{"name":doc.reference_name, 'docstatus':1, 'physically_disabled':1}, 'student_admission')

