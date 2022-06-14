import frappe,json
from frappe import msgprint, _
from frappe.utils import comma_and, get_link_to_form,get_link_to_form, getdate, formatdate
from frappe.model.document import Document
from erpnext import get_default_company
from erpnext.education.api import get_student_group_students
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday

class StudentAttendance(Document):
    def validate(self):
        if self.attendance_for == 'Hosteler':
            for d in frappe.get_all("Student Attendance",{"date":self.date,"student":self.student,"name":("!=",self.name),"docstatus": 1}):
                frappe.throw("Attendance Already Exist <b>{0}</b>".format(d.name))
        self.validate_date()
        self.set_date()
        self.set_student_group()
        self.validate_student()
        self.validate_duplication()
        self.validate_is_holiday()

    def on_submit(self):
        self.update_course_schedule()

    def set_date(self):
        if self.course_schedule:
            self.date = frappe.db.get_value('Course Schedule', self.course_schedule, 'schedule_date')

    def validate_date(self):
        if not self.hostel_leave_application and getdate(self.date) > getdate():
            frappe.throw(_('Attendance cannot be marked for future dates.'))

        if self.student_group:
            academic_year = frappe.db.get_value('Student Group', self.student_group, 'academic_year')
            if academic_year:
                year_start_date, year_end_date = frappe.db.get_value('Academic Year', academic_year, ['year_start_date', 'year_end_date'])
                if year_start_date and year_end_date:
                    if getdate(self.date) < getdate(year_start_date) or getdate(self.date) > getdate(year_end_date):
                        frappe.throw(_('Attendance cannot be marked outside of Academic Year {0}').format(academic_year))

    def set_student_group(self):
        if self.course_schedule:
            self.student_group = frappe.db.get_value('Course Schedule', self.course_schedule, 'student_group')

    def validate_student(self):
        if self.course_schedule:
            student_group = frappe.db.get_value('Course Schedule', self.course_schedule, 'student_group')
        else:
            student_group = self.student_group
        student_group_students = [d.student for d in get_student_group_students(student_group)]
        if student_group and self.student not in student_group_students:
            student_group_doc = get_link_to_form('Student Group', student_group)
            frappe.throw(_('Student {0}: {1} does not belong to Student Group {2}').format(
                frappe.bold(self.student), self.student_name, frappe.bold(student_group_doc)))

        if self.attendance_for == 'Hosteler' and not frappe.db.count("Hostel Allotment",{"docstatus":1,"student":self.student}):
            frappe.throw("Hostel Allotment not exist for Student")


    def validate_duplication(self):
        """Check if the Attendance Record is Unique"""
        attendance_record = None
        if self.course_schedule:
            attendance_record = frappe.db.exists('Student Attendance', {
                'student': self.student,
                'course_schedule': self.course_schedule,
                'docstatus': ('!=', 2),
                'name': ('!=', self.name)
            })
        else:
            attendance_record = frappe.db.exists('Student Attendance', {
                'student': self.student,
                'student_group': self.student_group,
                'date': self.date,
                'docstatus': ('!=', 2),
                'name': ('!=', self.name),
                'course_schedule': ''
            })

        if attendance_record:
            record = get_link_to_form('Student Attendance', attendance_record)
            frappe.throw(_('Student Attendance record {0} already exists against the Student {1}')
                .format(record, frappe.bold(self.student)), title=_('Duplicate Entry'))

    def validate_is_holiday(self):
        holiday_list = get_holiday_list()
        if is_holiday(holiday_list, self.date):
            frappe.throw(_('Attendance cannot be marked for {0} as it is a holiday.').format(
                frappe.bold(formatdate(self.date))))

    def update_course_schedule(self):
        if self.course_schedule and self.status=="Present":
            course_schedule=frappe.get_doc("Course Schedule",self.course_schedule)
            course_schedule.append("student_paper_code",{
                "student":self.student,
                "student_name":self.student_name
            })
            course_schedule.save()

@frappe.whitelist()
def get_student_details(student):
    data={}
    for allotment in frappe.get_all("Hostel Allotment",{"student":student,"docstatus":1},["building", "to_room","room_type", "floor"]):
        data.update(allotment)
    return data

def get_holiday_list(company=None):
    if not company:
        company = get_default_company() or frappe.get_all('Company')[0].name

    holiday_list = frappe.get_cached_value('Company', company,  'default_holiday_list')
    if not holiday_list:
        frappe.throw(_('Please set a default Holiday List for Company {0}').format(frappe.bold(get_default_company())))
    return holiday_list

@frappe.whitelist()
def get_course_schedule(doctype, txt, searchfield, start, page_len, filters):
    fltr = {}
    lst = []
    dct = {}
    if txt:
        fltr.update({"course":txt})
    for i in frappe.get_all("Student Paper Code",{'student':filters.get("student"),"parenttype":"Course Schedule"},['parent']):
        fltr.update({"name":i.get("parent")})
        for j in frappe.get_all("Course Schedule",fltr,["course"]):
            if i.parent not in lst and j.course not in lst:
                lst.append(i.parent)
                lst.append(j.course)
                dct.update({i.parent:j.course})

    return [(d,y) for d,y in dct.items()]

@frappe.whitelist()
def get_course(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                            Select 
                                    enroll_cr.course,
                                    enroll_cr.course_name,
                                    enroll_cr.course_code
                            from `tabProgram Enrollment` enroll
                            left join `tabProgram Enrollment Course` enroll_cr on enroll.name=enroll_cr.parent 
                            where enroll.student='{0}' and enroll.docstatus=1  and (enroll_cr.course LIKE %(txt)s or enroll_cr.course_name LIKE %(txt)s or enroll_cr.course_code LIKE %(txt)s) 
                            GROUP BY enroll_cr.course
                        """.format(filters.get("student")),dict(txt="%{}%".format(txt)))    

def validate(doc,method):
    for d in frappe.get_all("Student Attendance",{"date":doc.date,"student":doc.student,"student_group":doc.student_group,"name":("!=",doc.name),"docstatus": 1}):
        print("@@@@@@@@@@ d",d)
        frappe.throw("Attendance Already Exist <b>{0}</b>".format(d.name))

@frappe.whitelist()
def mark_attendance(students_present, students_absent, course_schedule=None, student_group=None,building=None,hostel_category=None, date=None,attendance_for=None):
    """Creates Multiple Attendance Records.

    :param students_present: Students Present JSON.
    :param students_absent: Students Absent JSON.
    :param course_schedule: Course Schedule.
    :param student_group: Student Group.
    :param date: Date.
    """

    if student_group:
        academic_year = frappe.db.get_value('Student Group', student_group, 'academic_year')
        if academic_year:
            year_start_date, year_end_date = frappe.db.get_value('Academic Year', academic_year, ['year_start_date', 'year_end_date'])
            if getdate(date) < getdate(year_start_date) or getdate(date) > getdate(year_end_date):
                frappe.throw(_('Attendance cannot be marked outside of Academic Year {0}').format(academic_year))

    present = json.loads(students_present)
    absent = json.loads(students_absent)

    for d in present:
        make_attendance_records(d["student"], d["student_name"], "Present", course_schedule, student_group,building,hostel_category, date,attendance_for)

    for d in absent:
        make_attendance_records(d["student"], d["student_name"], "Absent", course_schedule, student_group,building,hostel_category, date,attendance_for)

    frappe.db.commit()
    frappe.msgprint(_("Attendance has been marked successfully."))


def make_attendance_records(student, student_name, status, course_schedule=None, student_group=None,building=None,hostel_category=None, date=None,attendance_for=None):
    """Creates/Update Attendance Record.

    :param student: Student.
    :param student_name: Student Name.
    :param course_schedule: Course Schedule.
    :param status: Status (Present/Absent)
    """
    student_attendance = frappe.get_doc({
        "doctype": "Student Attendance",
        "student": student,
        "course_schedule": course_schedule,
        "student_group": student_group,
        "date": date
    })
    if not student_attendance:
        student_attendance = frappe.new_doc("Student Attendance")
    student_attendance.student = student
    student_attendance.student_name = student_name
    student_attendance.course_schedule = course_schedule
    student_attendance.student_group = student_group
    student_attendance.date = date
    student_attendance.status = status

    if attendance_for and building:
        student_attendance.building=building
        
        for d in frappe.get_all("Hostel Allotment",{"student":student,"docstatus":1,"building":building},['name','to_room']):
            student_attendance.hostel_room=d.to_room

    student_attendance.attendance_for=attendance_for if attendance_for else "Day Scholar"
    student_attendance.save()
    student_attendance.submit()


@frappe.whitelist()
def get_hostel_students(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                            SELECT student,student_name FROM `tabHostel Allotment` 
                            WHERE docstatus=1 and (student like %(txt)s or student_name like %(txt)s) 
                                And student NOT IN(SELECT student FROM `tabHostel Deallotment` where docstatus=1)
            """,{'txt': '%%%s%%' % txt})