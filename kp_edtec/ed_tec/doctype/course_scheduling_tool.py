from distutils.log import debug
import frappe
import calendar
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, getdate
from erpnext.education.utils import OverlapError
class CourseSchedulingTool(Document):

    @frappe.whitelist()
    def schedule_course(self):
        """Creates course schedules as per specified parameters"""

        course_schedules = []
        course_schedules_errors = []
        rescheduled = []
        reschedule_errors = []

        self.validate_mandatory()
        self.validate_date()
        self.instructor_name = frappe.db.get_value(
            "Instructor", self.instructor, "instructor_name")

        group_based_on, course = frappe.db.get_value(
            "Student Group", self.student_group, ["group_based_on", "course"])

        if group_based_on == "Course":
            self.course = course

        if self.reschedule:
            rescheduled, reschedule_errors = self.delete_course_schedule(
                rescheduled, reschedule_errors)

        date = self.course_start_date
        no_error=True
        while date < self.course_end_date:
            if self.day == calendar.day_name[getdate(date).weekday()]:
                course_schedule = self.make_course_schedule(date)
                try:
                    try:
                        course_schedule.save()
                    except:
                        self.instructor=""
                        self.instructor_name=""
                        no_error=False
                except OverlapError:
                    print('fail')
                    course_schedules_errors.append(date)
                else:
                    course_schedules.append(course_schedule)

                date = add_days(date, 7)
            else:
                date = add_days(date, 1)
        if no_error:
            return dict(
                course_schedules=course_schedules,
                course_schedules_errors=course_schedules_errors,
                rescheduled=rescheduled,
                reschedule_errors=reschedule_errors
            )

    def validate_mandatory(self):
        """Validates all mandatory fields"""

        fields = ['course', 'room', 'instructor', 'from_time',
                  'to_time', 'course_start_date', 'course_end_date', 'day']
        for d in fields:
            if not self.get(d):
                frappe.throw(_("{0} is mandatory").format(
                    self.meta.get_label(d)))

    def validate_date(self):
        """Validates if Course Start Date is greater than Course End Date"""
        if self.course_start_date > self.course_end_date:
            frappe.throw(
                _("Course Start Date cannot be greater than Course End Date."))

    def delete_course_schedule(self, rescheduled, reschedule_errors):
        """Delete all course schedule within the Date range and specified filters"""

        schedules = frappe.get_list("Course Schedule",
            fields=["name", "schedule_date"],
            filters=[
                ["student_group", "=", self.student_group],
                ["course", "=", self.course],
                ["schedule_date", ">=", self.course_start_date],
                ["schedule_date", "<=", self.course_end_date]
            ]
        )

        for d in schedules:
            try:
                if self.day == calendar.day_name[getdate(d.schedule_date).weekday()]:
                    frappe.delete_doc("Course Schedule", d.name)
                    rescheduled.append(d.name)
            except:
                reschedule_errors.append(d.name)
        return rescheduled, reschedule_errors

    def make_course_schedule(self, date):
        """Makes a new Course Schedule.
        :param date: Date on which Course Schedule will be created."""

        course_schedule = frappe.new_doc("Course Schedule")
        course_schedule.student_group = self.student_group
        course_schedule.course = self.course
        course_schedule.instructor = self.instructor
        course_schedule.instructor_name = self.instructor_name
        course_schedule.room = self.room
        course_schedule.schedule_date = date
        course_schedule.from_time = self.from_time
        course_schedule.to_time = self.to_time
        if self.get("additional_instructors"):
            for ai in (self.get("additional_instructors"))["instructor_list"]:
                course_schedule.append("additional_instructor",ai)
        return course_schedule

@frappe.whitelist()
def get_instructor(doctype, txt, searchfield, start, page_len, filters):
    fltr={"course":filters.get("course")}
    lst = []
    if txt:
        fltr.update({"parent":['like', '%{}%'.format(txt)]})
    for i in frappe.get_all("Instructor Log",fltr,['parent']):
        if i.parent not in lst :
            lst.append(i.parent)
    return [(d, ) for d in lst]


@frappe.whitelist()
def get_course(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                            Select 
                                    enroll_cr.course,
                                    enroll_cr.course_name,
                                    enroll_cr.course_code
                            from `tabProgram Enrollment` enroll
                            left join `tabProgram Enrollment Course` enroll_cr on enroll.name=enroll_cr.parent 
                            where enroll.program='{0}' and enroll.docstatus=1  and (enroll_cr.course LIKE %(txt)s or enroll_cr.course_name LIKE %(txt)s or enroll_cr.course_code LIKE %(txt)s) 
                            GROUP BY enroll_cr.course
                        """.format(filters.get("program")),dict(txt="%{}%".format(txt)))    
