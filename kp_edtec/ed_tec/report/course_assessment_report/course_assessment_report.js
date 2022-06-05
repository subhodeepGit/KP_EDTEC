// Copyright (c) 2016, suraj varade and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Course Assessment Report"] = {
	"filters": [
		{
			"label":"Student Group",
			"fieldname":"student_group",
			"fieldtype":"Link",
			"options":"Student Group"
		},
		{
			"label":"Academic Year",
			"fieldname":"academic_year",
			"fieldtype":"Link",
			"options":"Academic Year"
		},
		{
			"label":"Academic Term",
			"fieldname":"academic_term",
			"fieldtype":"Link",
			"options":"Academic Term",
			"get_query": function() {
				return {
					filters: {
						'academic_year': frappe.query_report.get_filter_value('academic_year')
					}
				}
			}
		},
		{
			"label":"Programs",
			"fieldname":"programs",
			"fieldtype":"Link",
			"options":"Programs",
		},
		{
			"label":"Semester",
			"fieldname":"semester",
			"fieldtype":"Link",
			"options":"Program",
			"get_query": function() {
				return {
					filters: {
						'programs': frappe.query_report.get_filter_value('programs')
					}
				}
			}
		},
		{
			"label":"Course",
			"fieldname":"course",
			"fieldtype":"Link",
			"options":"Course",
			get_query: () => {
				return {
					"query": "kp_edtec.ed_tec.report.course_assessment_report.course_assessment_report.get_course",
					"filters": {
						'programs': frappe.query_report.get_filter_value('programs'),
					   'semester': frappe.query_report.get_filter_value('semester')
					  }
				}
			}
		},
		{
			"label":"Course Assessment Criteria",
			"fieldname":"assessment_criteria",
			"fieldtype":"Link",
			"options": "Assessment Criteria",
			get_query: () => {
				if(frappe.query_report.get_filter_value('course')){
					return {
						"query": "kp_edtec.ed_tec.report.course_assessment_report.course_assessment_report.get_assessment_criteria",
						"filters": {
							'course': frappe.query_report.get_filter_value('course'),
						  }
					}
				}
			}
		}
	],
    "formatter":function (value, row, column, data, default_formatter) {
       value = default_formatter(value, row, column, data, default_formatter);
       if (column.fieldname === "earned_marks") {
            value = "<p style='margin:0px;padding-left:0px;background-color:#5af25f!important;'>"+value+"</p>";
       }
       return value;
    },
}
