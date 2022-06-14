// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course Assessment', {
	setup: function(frm) {
			frm.set_query("course", function() {
				return {
					query: 'kp_edtec.kp_edtec.doctype.course_assessment.course_assessment.get_courses',
					filters: {
						"student":frm.doc.student,
						"academic_year":frm.doc.academic_year,
						"academic_term":frm.doc.academic_term
					}
				};
			});
			frm.set_query("assessment_criteria", function() {
				return {
					query: 'kp_edtec.kp_edtec.doctype.course_assessment.course_assessment.get_assessment_criteria',
					filters: {
						"student":frm.doc.student,
						"course":frm.doc.course
					}
				};
			});
			frm.set_query("exam_declaration", function() {
				if(frm.doc.student){
					return {
						query: 'kp_edtec.kp_edtec.doctype.course_assessment.course_assessment.get_exam_declaration',
						filters: {
							"student":frm.doc.student,
							"docstatus":1
						}
					};
				}
				else{
					frappe.msgprint("Please add student first.")
				}
			});
		
		frm.set_query("assessment_plan", function() {
			return {
				filters: {
					"programs":frm.doc.programs,
					"program":frm.doc.semester,
					"academic_year":frm.doc.academic_year,
					"docstatus":1,
					"exam_declaration":frm.doc.exam_declaration,
					"course":frm.doc.course
				}
			};
		});
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year,
				}
			};
		});
	},
	course:function(frm){
		if (frm.doc.student && frm.doc.course){
			frappe.call({
				method:"kp_edtec.kp_edtec.doctype.course_assessment.course_assessment.get_details",
				args: {
					student:frm.doc.student,
					course:frm.doc.course
				},
				callback: function(r) {
					if (r.message){
						frm.set_value("programs",r.message['programs'])
						frm.set_value("semester",r.message['program'])
						frm.set_value("academic_year",r.message['academic_year'])
						frm.set_value("academic_term",r.message['academic_term'])
					}
				}
		  })
		}

	  frm.trigger("get_total_marks");
	},
	assessment_plan:function(frm){
		if(frm.doc.assessment_plan){
			frappe.db.get_value("Exam Assessment Plan", {'name':frm.doc.assessment_plan, "docstatus":1},'assessment_criteria', resp => {
					frm.set_value("assessment_criteria",resp.assessment_criteria)
			})
		}
	},
	assessment_criteria:function(frm){
		frm.set_df_property("exam_declaration","reqd",0)
		if(frm.doc.assessment_criteria){
			frappe.db.get_value("Assessment Criteria", {'name':frm.doc.assessment_criteria},'depends_on_exam_declaration', resp => {
				if (resp.depends_on_exam_declaration==1){
					frm.set_df_property("exam_declaration","reqd",1)
				}
			})
		}
		frm.trigger("get_total_marks");
	},
	get_total_marks:function(frm){
		if (frm.doc.course && frm.doc.assessment_criteria){
			frappe.call({
				method: 'kp_edtec.kp_edtec.doctype.course_assessment.course_assessment.get_assessment_criteria_detail',
				args: {
					course:frm.doc.course,
					criteria:frm.doc.assessment_criteria
				},
				callback: function(r) {
					if (r.message){
						frm.set_value("total_marks",r.message['total_marks']);
					}
				}
			});
		}
	}
});
