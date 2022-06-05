// Copyright (c) 2022, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Continuous Evaluation Tool', {
	refresh:function(frm){
		frm.disable_save();
			frm.page.set_primary_action(("Submit"), function() {
			let html_values=cur_frm.fields_dict.student_inputs.wrapper;
			var continuous_evaluation={};
			continuous_evaluation["rows"]={};
			continuous_evaluation["criteria"]=frm.doc.assessment_criteria;
			continuous_evaluation["academic_year"]=frm.doc.academic_year;
			continuous_evaluation["academic_term"]=frm.doc.academic_term;
			continuous_evaluation["course"]=frm.doc.course;
			continuous_evaluation["course_name"]=frm.doc.course_name;
			continuous_evaluation["course_code"]=frm.doc.course_code;
			if(cur_frm.doc.students){
				(cur_frm.doc.students).forEach(resp => {
					var row={};
					
					row['student']=resp.student;
					row['student_name']=resp.student_name;
					row['roll_no']=resp.roll_no;
					row['registration_number']=resp.registration_number;
					// row['student_name']=resp.student_name;
					
					$(html_values).find(`[data-row="${resp.student}"].evaluation`).each(function(el, input){
						row['evaluation']=$(input).val();
					})
					
					$(html_values).find(`[data-row="${resp.student}"].grace_marks`).each(function(el, input){
						row['grace_marks']=$(input).val();
					})

					$(html_values).find(`[data-row="${resp.student}"].weightage_marks`).each(function(el, input){
						row['weightage_marks']=$(input).val();
					})

					$(html_values).find(`[data-row="${resp.student}"].final_marks`).each(function(el, input){
						row['final_marks']=$(input).val();
					})

					$(html_values).find(`[data-row="${resp.student}"].earned_credits`).each(function(el, input){
						row['earned_credits']=$(input).val();
					})
					
					$(html_values).find(`[data-row="${resp.student}"].earned_marks`).each(function(el, input){
						row['earned_marks']=$(input).val();
					})
					$(html_values).find(`[data-row="${resp.student}"].total_marks`).each(function(el, input){
						row['total_marks']=$(input).val();
					})
					$(html_values).find(`[data-row="${resp.student}"].total_credits`).each(function(el, input){
						row['total_credits']=$(input).val();
					})

					$(html_values).find(`[data-row="${resp.student}"].out_of_marks`).each(function(el, input){
						row['out_of_marks']=$(input).val();
					})
					continuous_evaluation['rows'][resp.student]=row;
				})
			}
			frappe.call({
				method: "kp_edtec.ed_tec.doctype.continuous_evaluation_tool.continuous_evaluation_tool.make_continuous_evaluation",
				args: {
					"continuous_evaluation":continuous_evaluation,
					}
			});
		});
	},
	setup: function(frm) {
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year,
				}
			};
		});
		frm.set_query('semester', function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
		frm.set_query('course', function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.continuous_evaluation_tool.continuous_evaluation_tool.get_courses',
				// 'ed_tec.ed_tec.doctype.program_enrollment.get_program_courses',
				// 'erpnext.education.doctype.program_enrollment.program_enrollment.get_program_courses',
				filters: {
					'semester': frm.doc.semester
					// 'program': frm.doc.semester
				}
			};
		});
	},
	academic_year:function(frm){
		frm.trigger("get_student_details");
	},
	academic_term:function(frm){
		frm.trigger("get_student_details");
	},
	programs:function(frm){
		frm.trigger("get_student_details");
	},
	semester:function(frm){
		frm.trigger("get_student_details");
	},
	course:function(frm){
		frm.trigger("get_student_details");
	},
	assessment_criteria: function(frm) {
		frm.trigger("get_student_details");
	},
	get_student_details:function(frm){
		frm.doc.students=[];
		$(frm.fields_dict.student_inputs.wrapper).empty();
		if(frm.doc.academic_year && frm.doc.academic_term && frm.doc.course && frm.doc.assessment_criteria && frm.doc.programs && frm.doc.semester) {
			frappe.call({
				method: "get_student_allocations",
				doc:frm.doc,
				callback: function(r) {
					if (r.message) {
						$(frm.fields_dict.student_inputs.wrapper).empty();
						frm.doc.students=r.message;
						var result_table = $(frappe.render_template('continuous_evaluation_tool', {
							frm: frm,
							students: r.message,
						}));
						result_table.appendTo(frm.fields_dict.student_inputs.wrapper);
					}
				}
			});
		}
	}
});
