import frappe,json
from frappe.model.mapper import get_mapped_doc
from kp_edtec.ed_tec.doctype.custom_naming_series import get_default_naming_series,make_autoname,_field_autoname,set_name_by_naming_series,_prompt_autoname,_format_autoname
from kp_edtec.ed_tec.doctype.user_permission import add_user_permission,delete_ref_doctype_permissions

def validate(doc,method):
    get_options_from_student(doc)
    duplicate_student_group(doc)

    if not doc.get("__islocal"):
        create_user_permission(doc)

def after_insert(doc,method):
    create_user_permission(doc)

def on_trash(doc,method):
    remove_permissions(doc)

def duplicate_student_group(doc):
    if doc.group_based_on=="Exam Declaration":
        for st_grp in frappe.get_all("Student Group",{"name":("!=",doc.name),"exam_declaration":doc.exam_declaration,"programs":doc.programs,"program":doc.program,"course":doc.course,"academic_year":doc.academic_year,"academic_term":doc.academic_term,"group_based_on":doc.group_based_on}):
            frappe.throw("Student Group Already Exists with Same Details <b>{0}</b>".format(st_grp.name))
    else:
        for st_grp in frappe.get_all("Student Group",{"name":("!=",doc.name),"programs":doc.programs,"program":doc.program,"academic_year":doc.academic_year,"academic_term":doc.academic_term,"group_based_on":doc.group_based_on}):
            frappe.throw("Student Group Already Exists with Same Details <b>{0}</b>".format(st_grp.name))

def get_options_from_student(doc):
    student_field = frappe.get_meta("Student").get_field("naming_series")
    student_group_field = frappe.get_doc('Custom Field', "Student Group-roll_number_series")
    student_group_field.options = student_field.options
    student_group_field.save()

@frappe.whitelist()
def create_student_group(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.group_based_on="Exam Declaration"
        target.exam_schedule_date = source.get("schedule_date")
    
    doclist = get_mapped_doc("Course Assessment Plan", source_name,     {
        "Course Assessment Plan": {
            "doctype": "Student Group",
            "field_map": {
                "from_time": "from_time",
                "to_time": "to_time",
                "room":"class_room"
            },
            "validation": {
                "docstatus": ["=", 1]
            }
        },
    }, target_doc,set_missing_values)

    return doclist

@frappe.whitelist()
def create_course_schedule(source_name, target_doc=None):
    def set_missing_values(source, target):
        if len(source.instructors)>0:
            target.instructor=source.instructors[0].instructor
            target.instructor_name=source.instructors[0].instructor_name
        if source.group_based_on == "Exam Declaration":
            target.is_exam_schedule = 1
            target.schedule_date = source.exam_schedule_date

    doclist = get_mapped_doc("Student Group", source_name,  {
        "Student Group": {
            "doctype": "Course Schedule",
            "field_map": {
                "class_room":"room"
            },
        },
    }, target_doc,set_missing_values)

    return doclist

# @frappe.whitelist()
# def create_course_schedule_when_exam_declaration(source_name, target_doc=None):
#     doclist = get_mapped_doc("Student Group", source_name,  {
#         "Student Group": {
#             "doctype": "Course Schedule",
#             "field_map": {
#                 "class_room":"room",
#                 "is_exam_schedule":1
#             },
#         },
#     }, target_doc,set_missing_values)

#     return doclist

@frappe.whitelist()
def get_student(programs,academic_term,max_strength):
    data_set = []
    for apl in frappe.get_all("Exam Application", {"docstatus":1,'current_program':programs,'academic_term':academic_term},['student','student_name']):
        data_set.append(apl)
    if max_strength == 0 and len(data_set) > 0:
        frappe.throw("Please add max strength.")
    if len(data_set) == 0:
        frappe.throw("Exam Application not exist.")
    strength = int(max_strength)
    return data_set[0:strength]

@frappe.whitelist()
def get_instructor(filters):
    filters=json.loads(filters)
    lst = []
    instructor=""
    fltr={"academic_year":filters.get("academic_year"),"course":filters.get("course")}
    if filters.get("apply_semester_filter"):
        fltr.update({"program":["IN",filters.get("semesters")]})
    for i in frappe.get_all("Instructor Log",filters=fltr,fields=['parent'],order_by="parent"):
        if i.parent not in lst:
            lst.append(i.parent)
            instructor+=("\n"+i.parent)
    return instructor


@frappe.whitelist()
def filter_student(doctype, txt, searchfield, start, page_len, filters):
    student=[]
    for d in frappe.get_all("Student Group Student",{"parent":filters.get("student_group")},["student"]):
        for stu in frappe.get_all("Student",{"name":d.student},["name","title"],as_list=1):
            student.append(stu)
    return student


@frappe.whitelist()
def get_courses(semester):
    courses=""
    for c in frappe.get_all("Program Course",filters={"parent":semester},fields=['course'],order_by="course"):
        courses+=("\n"+c.course)
    return courses

@frappe.whitelist()
def filter_courses(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Program Course",filters={"parent":filters.get("program"),'course': ['like', '%{}%'.format(txt)]},fields=['course','course_name'],order_by="idx",as_list=1)

@frappe.whitelist()
def get_courses_from_ed(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Exam Courses",filters={"parent":filters.get("exam_declaration")},fields=['courses','course_name',"course_code"],order_by="idx",as_list=1)

@frappe.whitelist()
def filter_programs(doctype, txt, searchfield, start, page_len, filters):
    lst=[]
    for d in frappe.get_all("Course",filters={"name":filters.get("course"),'programs': ['like', '%{}%'.format(txt)]},fields=['programs'],order_by="programs"):
        if d.programs not in lst:
            lst.append(d.programs)
    return [(d,) for d in lst]

@frappe.whitelist()
def get_courses_on_declaration(declaration):
    courses=""
    for c in frappe.get_all("Admit Card Course",filters={"parent":declaration},fields=['courses'],order_by="courses"):
        courses+=("\n"+c.courses)
    return courses
    
@frappe.whitelist()
def get_students(academic_year, group_based_on, academic_term=None, program=None, batch=None, student_category=None, course=None):
    enrolled_students = get_program_enrollment(academic_year, academic_term, program, batch, student_category, course)
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

@frappe.whitelist()
def get_student_based_on_exam_declaration(**args):
    student_list = []
    for declaration in frappe.get_all("Exam Declaration",{"name":args.get("exam_declaration")},['is_application_required','name']):
        if declaration.is_application_required:
            for exam_app in frappe.get_all("Exam Application",{"exam_declaration":declaration.name, 'docstatus':1},['name','student','student_name']):
                for cr in frappe.get_all("Exam Application Courses",{"parent":exam_app.name,"course":args.get("course")}):
                    student_list.append(exam_app)
        else:
            filters={"semester":args.get("semester"),"academic_year":args.get("academic_year"),"academic_term":args.get("academic_term"),"course":args.get("course")}
            for cr_enroll in frappe.get_all("Course Enrollment",filters=filters,fields=["student","student_name"],group_by="student"):
                if frappe.db.get_value("Student", cr_enroll.student, "enabled"):
                    cr_enroll.update({"active": 1})
                else:
                    cr_enroll.update({"active": 0})
                student_list.append(cr_enroll)
    return student_list

def get_program_enrollment(academic_year, academic_term=None, program=None, batch=None, student_category=None, course=None):
    condition1 = " "
    condition2 = " "
    if academic_term:
        condition1 += " and pe.academic_term = %(academic_term)s"
    if program:
        condition1 += " and pe.program = %(program)s"
    if batch:
        condition1 += " and pe.student_batch_name = %(batch)s"
    if student_category:
        condition1 += " and pe.student_category = %(student_category)s"
    if course:
        condition1 += " and pe.name = pec.parent and pec.course = %(course)s"
        condition2 = ", `tabProgram Enrollment Course` pec"
    
    return frappe.db.sql('''
        select
            pe.student, pe.student_name
        from
            `tabProgram Enrollment` pe {condition2}
        where
            (pe.is_provisional_admission IS NULL or pe.is_provisional_admission="No") and
            pe.academic_year = %(academic_year)s  {condition1}
        order by
            pe.student_name asc
        '''.format(condition1=condition1, condition2=condition2),
                ({"academic_year": academic_year, "academic_term":academic_term, "program": program, "batch": batch, "student_category": student_category, "course": course}), as_dict=1)

@frappe.whitelist()
def get_student_based_on_combined_course(filters):
    filters=json.loads(filters)
    data_set = []
    programs_list=[d.get("programs") for d in filters.get("programs_list")]

    for apl in frappe.get_all("Course Enrollment", {'course':filters.get("course")},['student','student_name','program_enrollment']):
        for pr in frappe.get_all("Program Enrollment",{"name":apl.program_enrollment,"programs":["IN",programs_list],"academic_year":filters.get("academic_year"),'docstatus':1,"is_provisional_admission":["IN",[None,"No"]]}):
            data_set.append(apl)
    strength = int(filters.get("max_strength"))
    return data_set[0:strength]

@frappe.whitelist()
def get_student_based_on_activity(academic_year, academic_term=None, programs=None,program=None):
    enrolled_students = get_program_enrollment(academic_year, academic_term, program)
    if enrolled_students:
        student_list = []
        for s in enrolled_students:
            if frappe.db.get_value("Student", s.student, "enabled"):
                s.update({"active": 1})
            else:
                s.update({"active": 0})
            student_list.append(s.values())
        return student_list
    else:
        return []

@frappe.whitelist()
def generate_roll_no(selected_naming,name,students):
    
    doc=frappe.get_doc("Student Group",name)
    autoname=selected_naming
    _autoname = autoname.lower()
    students=json.loads(students)
    for (idx,d) in enumerate(students,1):
        if frappe.db.get_value("Student",d.get("student"),"renamed")==0:
            new_name=get_name(_autoname,autoname,doc)
            frappe.rename_doc("Student",d.get("student"),new_name)
            frappe.db.set_value("Student",new_name,"renamed",1)
        show_progress(students,('Renamed: {0}').format(d.get("student_name")), idx, d)

    return "ok"
def get_name(_autoname,autoname,doc):
    if _autoname.startswith("field:"):
        return _field_autoname(autoname, doc)
    elif _autoname.startswith("naming_series:"):
        return set_name_by_naming_series(doc,autoname)
    elif _autoname.startswith("prompt"):
        return _prompt_autoname(autoname, doc)
    elif _autoname.startswith("format:"):
        return _format_autoname(autoname, doc)
    elif "#" in autoname:
        return make_autoname(autoname, doc=doc)
    else:
        return make_autoname(autoname+".#####", "", doc)

def set_name_by_naming_series(doc,autoname):
    """Sets name by the `naming_series` property"""

    return make_autoname(autoname+".#####", "", doc)



def show_progress(docnames, message, i, description):
    n = len(docnames)
    frappe.publish_progress(
        float(i) * 100 / n,
        title = message,
        description = description
    )


@frappe.whitelist()
def get_student_emails(students):
    students=json.loads(students)
    recipients=""
    for stu in students:
        recipients+=(frappe.db.get_value("Student",{"name":stu.get("student")},"student_email_id")+",")
    return recipients

@frappe.whitelist()
def get_semester_by_exam_declaration(doctype, txt, searchfield, start, page_len, filters):
    return frappe.get_all("Examination Semester",filters={"parent":filters.get("exam_declaration"),'semester': ['like', '%{}%'.format(txt)]},fields=['semester'],order_by="idx",as_list=1)

@frappe.whitelist()
def filter_programs_by_course(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                    Select distinct(pr.programs)
                    From `tabProgram Course` cr
                    left join `tabProgram` pr on pr.name=cr.parent
                    Where cr.course='{0}' and (pr.programs like %(txt)s) 
    """.format(filters.get('course')),{'txt': '%%%s%%' % txt})

def create_user_permission(doc):
    for d in doc.get("instructors"):
        for instr in frappe.get_all("Instructor",{"name":d.instructor},['employee']):
            for emp in frappe.get_all("Employee",{"name":instr.employee},['user_id']):
                if emp.user_id:
                    add_user_permission(doc.doctype,doc.name,emp.user_id,doc)

def remove_permissions(doc):
    delete_ref_doctype_permissions(["Student Group"],doc)