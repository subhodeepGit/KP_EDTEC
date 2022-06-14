from . import __version__ as app_version

app_name = "kp_edtec"
app_title = "Kp Edtec"
app_publisher = "SOUL"
app_description = "SOUL"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "soul@soulunileaders.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kp_edtec/css/kp_edtec.css"
app_include_js = [
                    "/assets/kp_edtec/core_js/breadcrumbs.js",
                    "/assets/kp_edtec/core_js/common.js",
                    "/assets/js/kp_edtec.min.js"
                ]

# include js, css files in header of web template
# web_include_css = "/assets/kp_edtec/css/kp_edtec.css"
# web_include_js = "/assets/kp_edtec/js/kp_edtec.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "kp_edtec/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
                "Course":"public/js/course.js",
                "Course Enrollment":"public/js/course_enrollment.js",
                "Course Schedule": "public/js/course_schedule.js",
                "Course Scheduling Tool": "public/js/course_scheduling_tool.js",
                "Fees" : "public/js/fees.js",
                "Fee Schedule":"public/js/fee_schedule.js",
                "Fee Structure" : "public/js/fee_structure.js",
                "Instructor":"public/js/instructor.js",
                "Program Enrollment":"public/js/program_enrollment.js",
                "Program":"public/js/program.js",
                "Student":"public/js/student.js",
                "Student Admission":"public/js/student_admission.js",
                "Student Applicant":"public/js/student_applicant.js",
                "Student Attendance":"public/js/student_attendance.js",
                "Student Attendance Tool":"public/js/student_attendance_tool.js",
                "Student Group": "public/js/student_group.js",
                "Student Leave Application":"public/js/student_leave_application.js",
                "Student Log":"public/js/student_log.js",
                "Topic":"public/js/topic.js",
                "User":"public/js/user.js",
            }

doctype_list_js = {
    "Branch Sliding Application": "kp_edtec/kp_edtec/doctype/branch_sliding_application/branch_sliding_application_list.js",
    "Fees":"public/js/fees_list.js",
    "Student Attendance":"public/js/student_attendance_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------
after_migrate = [
        'kp_edtec.patches.migrate_patch.set_translation',
        'kp_edtec.patches.migrate_patch.add_roles',
        'kp_edtec.patches.migrate_patch.set_custom_role_permission',
        'kp_edtec.kp_edtec.delete_doc_if_linked.execute'
]

# fixtures = [
# 	{"dt": "Custom DocPerm", "filters": [
# 		[
# 			"parent", "not in", [
# 				"DocType"
# 			]
# 		]
# 	]},
#     {"dt": "Role"},
# #     # {"dt": "Fee Type"},
# #     # {"dt": "Workflow"}
# ]
# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "kp_edtec.install.before_install"
after_install = "kp_edtec.patches.get_phone_codes.execute"

# Uninstallation
# ------------

# before_uninstall = "kp_edtec.uninstall.before_uninstall"
# after_uninstall = "kp_edtec.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kp_edtec.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Academic Calender": {
        "validate": "kp_edtec.kp_edtec.validations.academic_calender.validate"
    },
    "Academic Calendar Template": {
        "validate": "kp_edtec.kp_edtec.validations.academic_calender_template.validate"
    },
    "Branch sliding Declaration": {
        "validate": "kp_edtec.kp_edtec.validations.branch_sliding_declaration.validate"
    },
    "Branch Sliding Application": {
        "validate": "kp_edtec.kp_edtec.validations.branch_sliding_application.validate"
    },
    "Course": {
        "validate": ["kp_edtec.kp_edtec.validations.course.validate",
                     "kp_edtec.kp_edtec.doctype.course.validate"]
    },
    "Course Assessment": {
        "validate": "kp_edtec.kp_edtec.validations.course_assessment.validate"
    },
    "Course Assessment Result": {
        "validate": "kp_edtec.kp_edtec.validations.course_assessment_result.validate"
    },
    "Course Enrollment":{
       "after_insert":"kp_edtec.kp_edtec.doctype.course_enrollment.after_insert",
       "validate":"kp_edtec.kp_edtec.doctype.course_enrollment.validate",
       "on_trash":"kp_edtec.kp_edtec.doctype.course_enrollment.on_trash"
    },
	"Course Schedule": {
		"on_update": "kp_edtec.kp_edtec.doctype.course_schedule.on_change",
        "validate": "kp_edtec.kp_edtec.validations.course_schedule.validate"
	},
    "Counselling Structure":{
        "validate":"kp_edtec.kp_edtec.validations.counselling_structure.validate"
    },
    "Exam Assessment Plan": {
        "validate": "kp_edtec.kp_edtec.validations.exam_assesment_plan.validate"
    },
    "Exam Application":{
        "validate":"kp_edtec.kp_edtec.validations.exam_application.validate"
    },
    "Exam Declaration":{
        "validate":"kp_edtec.kp_edtec.validations.exam_declaration.validate"
    },
    "Exchange Program Declaration":{
        "validate":"kp_edtec.kp_edtec.validations.exchange_program_declaration.validate"
    },
    "Exam Paper Setting":{
        "validate":"kp_edtec.kp_edtec.validations.exam_paper_setting.validate"
    },
    "Fees":{
        "on_submit":"kp_edtec.kp_edtec.doctype.fees.on_submit",
        "validate":"kp_edtec.kp_edtec.doctype.fees.validate",
        "on_cancel":"kp_edtec.kp_edtec.doctype.fees.on_cancel"
    },
    "Fee Structure":{
        "validate":"kp_edtec.kp_edtec.validations.fee_structure.validate"
    },
    "Feedback":{
        "validate":"kp_edtec.kp_edtec.validations.feedback.validate"
    },
    "Fee Schedule":{
        "validate":"kp_edtec.kp_edtec.validations.fee_schedule.validate"
    },
    "Final Result Declaration":{
        "validate":"kp_edtec.kp_edtec.validations.final_result_declaration.validate"
    },
    "Instructor":{
        "validate":["kp_edtec.kp_edtec.doctype.instructor.validate",
        "kp_edtec.kp_edtec.validations.instructor.validate"],
        "on_trash":"kp_edtec.kp_edtec.doctype.instructor.on_trash"
    },
    "Mentor Allocation": {
        "validate": "kp_edtec.kp_edtec.validations.mentor_allocation.validate"
    },
    "Placement Drive":{
        "validate":"kp_edtec.kp_edtec.validations.placement_drive.validate"
    },
    "Placement Drive Application":{
        "validate":"kp_edtec.kp_edtec.validations.placement_drive_application.validate"
    },
    "Photocopy Application":{
        "validate":"kp_edtec.kp_edtec.validations.photocopy_application.validate"
    },
    "Post Exam Declaration":{
        "validate":"kp_edtec.kp_edtec.validations.post_exam_declaration.validate"
    },
    "Program":{
        "after_insert":"kp_edtec.kp_edtec.doctype.program.after_insert",
        "validate":"kp_edtec.kp_edtec.doctype.program.validate",
        "on_trash":"kp_edtec.kp_edtec.doctype.program.on_trash"
    },
    "Programs":{
        "validate":"kp_edtec.kp_edtec.validations.programs.validate"
    },
    "Program Enrollment":{
        "on_submit":["kp_edtec.kp_edtec.doctype.program_enrollment.on_submit"],
        "on_cancel":["kp_edtec.kp_edtec.doctype.program_enrollment.on_cancel"],
        "on_change":"kp_edtec.kp_edtec.doctype.program_enrollment.on_change",
        "validate":["kp_edtec.kp_edtec.validations.program_enrollment.validate",
                    "kp_edtec.kp_edtec.doctype.program_enrollment.validate"]
    },
   
    "Reevaluation Application":{
        "validate":"kp_edtec.kp_edtec.validations.reevalution_application.validate"
    },
    "Student":{
        "after_insert":"kp_edtec.kp_edtec.doctype.student.after_insert",
        "on_trash":"kp_edtec.kp_edtec.doctype.student.on_trash",
        "on_change":"kp_edtec.kp_edtec.doctype.student.on_update",
        "validate":"kp_edtec.kp_edtec.doctype.student.validate"
    },
    "Student Admit Card":{
        "validate":"kp_edtec.kp_edtec.validations.student_admit_card.validate"
    },
    "Student Group":{
        "validate":["kp_edtec.kp_edtec.validations.student_group.validate","kp_edtec.kp_edtec.doctype.student_group.validate"],
        "after_insert":"kp_edtec.kp_edtec.doctype.student_group.after_insert",
        "on_trash":"kp_edtec.kp_edtec.doctype.student_group.on_trash"
    },
    "Student Log":{
        "validate":"kp_edtec.kp_edtec.validations.student_log.validate"
    },
    "Student Exchange Applicant":{
        "validate":"kp_edtec.kp_edtec.validations.student_exchange_applicant.validate"
    },
    "Student Exam Block List":{
        "validate":"kp_edtec.kp_edtec.validations.student_exam_block_list.validate"
    },
    "Student Leave Application":{
        "validate":"kp_edtec.kp_edtec.validations.student_leave_application.validate"
    },
    "Student Applicant":{
        "validate":["kp_edtec.kp_edtec.doctype.student_applicant.validate",
                    "kp_edtec.kp_edtec.validations.student_applicant.validate"],
        "on_change":"kp_edtec.kp_edtec.doctype.student_applicant.on_update",
        "on_submit":"kp_edtec.kp_edtec.validations.student_applicant.on_submit"
    },
    "Student Admission":{
        "validate":["kp_edtec.kp_edtec.doctype.student_admission.validate",
        "kp_edtec.kp_edtec.validations.student_admission.validate"]
    },
    "Student Attendance":{
        "validate":["kp_edtec.kp_edtec.doctype.student_attendance.validate"]
    },
    ("Student Admit Card"):{
        "after_insert":"kp_edtec.kp_edtec.doctype.user_permission.after_insert",
        "on_trash":"kp_edtec.kp_edtec.doctype.user_permission.on_trash"
    },
    "Payment Entry": {
		"validate": "kp_edtec.kp_edtec.validations.payment_entry.validate",
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
		"kp_edtec.kp_edtec.doctype.student_blocklist_check.student_blocklist_check",
        "kp_edtec.kp_edtec.doctype.exam_assessment_plan.exam_assessment_plan.make_exam_paper_setting_by_paper_setting_date"
	]

}

# Testing
# -------

# before_tests = "kp_edtec.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.education.api.get_course_schedule_events": "kp_edtec.kp_edtec.doctype.course_schedule.get_course_schedule_events",
    "erpnext.education.api.mark_attendance": "kp_edtec.kp_edtec.doctype.student_attendance.mark_attendance"
}
override_doctype_class = {
	"Course Scheduling Tool": "kp_edtec.kp_edtec.doctype.course_scheduling_tool.CourseSchedulingTool",
    "Student Attendance": "kp_edtec.kp_edtec.doctype.student_attendance.StudentAttendance",
    "Employee":"kp_edtec.kp_edtec.doctype.employee.Employee",
    "Course Schedule": "kp_edtec.kp_edtec.doctype.course_schedule.CourseSchedule",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
    "Academic Year": "kp_edtec.kp_edtec.dashboard.academic_year_dashboard.get_data",
    "Academic Term": "kp_edtec.kp_edtec.dashboard.academic_term_dashboard.get_data",
    "Assessment Group":"kp_edtec.kp_edtec.dashboard.assessment_group_dashboard.get_data",
    "Course": "kp_edtec.kp_edtec.dashboard.course_dashboard.get_data",
    "Grading Scale": "kp_edtec.kp_edtec.dashboard.grading_scale_dashboard.get_data",
    "Hostel Admission": "kp_edtec.kp_edtec.dashboard.hostel_admission_dashboard.get_data",
    "Instructor": "kp_edtec.kp_edtec.dashboard.instructor_dashboard.get_data",
    "Program": "kp_edtec.kp_edtec.dashboard.program_dashboard.get_data",
    "Room": "kp_edtec.kp_edtec.dashboard.room_dashboard.get_data",
    "Student": "kp_edtec.kp_edtec.dashboard.student_dashboard.get_data",
    "Student Group": "kp_edtec.kp_edtec.dashboard.student_group_dashboard.get_data",
	"User": "kp_edtec.kp_edtec.dashboard.user_dashbaord.get_data",
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"kp_edtec.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
