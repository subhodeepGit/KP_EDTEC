// Copyright (c) 2016, suraj varade and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Course Wise Result"] = {
	"filters": [
			{
				"fieldname":"programs",
				"label":"Programs",
				"fieldtype":"Link",
				"options":"Programs",
				"reqd":1
			},
			{
				"fieldname":"semester",
				"label":"Semester",
				"fieldtype":"Link",
				"options":"Program",
				get_query: () => {
					return {
						filters: {
							'programs': frappe.query_report.get_filter_value('programs')
						}
					};
				}
			},
			{
				"fieldname":"course",
				"label":"Course",
				"fieldtype":"Link",
				"options":"Course",
				get_query: () => {
					if (frappe.query_report.get_filter_value('semester')){
						return {
							query: 'kp_edtec.ed_tec.doctype.program_enrollment.get_courses',
							filters: {
								"semester":frappe.query_report.get_filter_value('semester')
							}
						};
					}
				}
			},
			{
				"fieldname":"academic_year",
				"label":"Academic Year",
				"fieldtype":"Link",
				"options":"Academic Year",
				"reqd":1
			},
			{
				"fieldname":"academic_term",
				"label":"Academic Term",
				"fieldtype":"Link",
				"options":"Academic Term",
				get_query: () => {
					return {
						filters: {
							'academic_year': frappe.query_report.get_filter_value('academic_year')
						}
					};
				}
			},
			{
				"fieldname":"grading_scale",
				"label":"Grading Scale",
				"fieldtype":"Link",
				"options":"Grading Scale"
			}
	]
};
