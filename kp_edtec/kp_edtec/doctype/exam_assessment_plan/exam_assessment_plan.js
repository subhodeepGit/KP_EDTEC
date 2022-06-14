// Copyright (c) 2022, suraj varade and contributors
// For license information, please see license.txt
cur_frm.dashboard.add_transactions([
	{
		'items': [
			'Exam Paper Setting'
		]
	},
]);

frappe.ui.form.on('Exam Assessment Plan', {
	setup:function(frm) {
		frm.set_query('academic_term', function() {
			return {
				filters: {
					'academic_year': frm.doc.academic_year
				}
			};
		});
		frm.set_query('exam_declaration', function(){
			return {
				filters: {
					docstatus: 1,
					disabled:0
				}
			};
		});
		frm.set_query('grading_scale', function(){
			return {
				filters: {
					docstatus: 1
				}
			};
		});
		frm.set_query('program',function() {
		    return {
				query: 'kp_edtec.kp_edtec.doctype.exam_assessment_plan.exam_assessment_plan.get_sem',
				filters: {
					"exam_declaration":frm.doc.exam_declaration
				}
			};
		});
		frm.set_query('student_group',function() {
		    return {
				filters: {
					"group_based_on":"Exam Declaration"
				}
			};
		});
		frm.set_query('paper_setter','examiners_list', function(frm, cdt, cdn) {
		    var d = locals[cdt][cdn];
		    return {
		    	query: 'kp_edtec.kp_edtec.doctype.exam_assessment_plan.exam_assessment_plan.filter_paper_setter',
				filters: {
					"course":d.course
				}
			};
		});
		frm.set_query('moderator','moderator_list', function() {
		    return {
		    	query: 'kp_edtec.kp_edtec.doctype.exam_assessment_plan.exam_assessment_plan.filter_paper_setter'
			};
		});
			frm.set_query("course","course_assessment_plan_item",function() {
				return {
					query: 'kp_edtec.kp_edtec.doctype.exam_assessment_plan.exam_assessment_plan.get_courses',
					filters: {
						"program":frm.doc.program,
						"assessment_criteria":frm.doc.assessment_criteria,
						"exam_declaration":frm.doc.exam_declaration
					}
				};
			});
		
		

		frm.fields_dict["examiners_list"].grid.get_field("course").get_query = function(doc, cdt, cdn){
		var courses = frm.doc.course_assessment_plan_item.map(d => d.course);
			return {
				filters: {
					"name":["IN",courses],
				}
			}
		};

		frm.fields_dict["moderator_list"].grid.get_field("course").get_query = function(doc, cdt, cdn){
			var courses = frm.doc.course_assessment_plan_item.map(d => d.course);
			return {
				filters: {
					"name":["IN",courses],
				}
			}
		};
	},

	refresh: function(frm) {
		// if (frm.doc.docstatus == 1) {
		// 	frm.add_custom_button(__('Course Assessment Result Tool'), function() {
		// 		frappe.route_options = {
		// 			exam_assessment_plan: frm.doc.name,
		// 			student_group: frm.doc.student_group
		// 		}
		// 		frappe.set_route('Form', 'Course Assessment Result Tool');
		// 	}, __('Tools'));
			
		// 	// frm.add_custom_button(__("Student Group"), function() {
		// 	// 	frappe.model.open_mapped_doc({
		// 	// 		method: "kp_edtec.kp_edtec.doctype.student_group.create_student_group",
		// 	// 		frm: frm,
		// 	// 	});
		// 	// }, __('Create'))
			
		// }
		if (!frm.doc.__islocal){
			frm.add_custom_button(__("Paper Setting Now"), function() {
				frappe.call({
					method: 'create_exam_paper_setter',
					doc:frm.doc,
					callback: function(r) {
						if (r.message) {
							frappe.msgprint("Records Created")
						}
					}
				});
			}, __('Create'))
		}
	},
	exam_declaration:function(frm){
        frm.trigger("get_courses");
	},
	assessment_criteria:function(frm){
        frm.trigger("get_courses");
	},
	program:function(frm){
        frm.trigger("get_courses");
	},
	student_group:function(frm){
		if (frm.doc.student_group) {
			frappe.call({
				method: 'kp_edtec.kp_edtec.doctype.exam_assessment_plan.exam_assessment_plan.course_assessment_credit',
				args: {
					student_group: frm.doc.student_group
				},
				callback: function(r) {
					if (r.message) {
						frm.doc.course_assessment_credit = [];
						$.each(r.message, function(i, d) {
							var row = frm.add_child("course_assessment_credit")
							row.course = d.courses;
							row.credit=d.total;
						});
					}
					refresh_field('course_assessment_credit');

				}
			});
		}
	},
	get_courses:function(frm){
		if(frm.doc.exam_declaration && frm.doc.assessment_criteria && frm.doc.program){
        	frappe.model.with_doc("Exam Declaration", frm.doc.exam_declaration, function() {
	            var tabletransfer= frappe.model.get_doc("Exam Declaration", frm.doc.exam_declaration)
	            if(tabletransfer.courses_offered.length > 0){
	            	frm.clear_table("course_assessment_plan_item");
		            $.each(tabletransfer.courses_offered, function(index, row){
						if (row.semester==frm.doc.program){
							var d = frm.add_child("course_assessment_plan_item");
							d.course = row.courses;
							d.course_name = row.course_name ;
							d.course_code = row.course_code;
							if (d.course && frm.doc.assessment_criteria){
								frappe.call({
									method: 'kp_edtec.kp_edtec.doctype.exam_assessment_plan.exam_assessment_plan.get_assessment_criteria_detail',
									args: {
										course:d.course,
										criteria:frm.doc.assessment_criteria
									},
									callback: function(r) {
										if (r.message){
											d.total_marks=r.message['total_marks']
											d.total_credit=r.message['credits']
											d.passing_marks=r.message['passing_marks']
											refresh_field("total_marks", d.name, d.parentfield);
											refresh_field("total_credit", d.name, d.parentfield);
											refresh_field("passing_marks", d.name, d.parentfield);
										}
									}
								});
							}
							frm.refresh_field("course_assessment_plan_item");
						}
		            });
	            }
	        });
        }
	}

});
frappe.ui.form.on("Course Assessment Credit", "theory", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.maximum_score=((d.theory||0)+(d.practical||0))
	refresh_field("maximum_score", d.name, d.parentfield);
});
frappe.ui.form.on("Course Assessment Credit", "practical", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.maximum_score=((d.theory||0)+(d.practical||0))
	refresh_field("maximum_score", d.name, d.parentfield);
});
frappe.ui.form.on("Course Assessment Plan Item", "course", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if(!frm.doc.program && frm.doc.assessment_criteria && frm.doc.exam_declaration){
    	frappe.msgprint("Please enter semester")
    }
	if (!frm.doc.assessment_criteria){
		frappe.msgprint("Select Assessment Criteria First");
		d.course='';
		refresh_field("course", d.name, d.parentfield);
	}
	if (d.course && frm.doc.assessment_criteria){
		frappe.call({
			method: 'kp_edtec.kp_edtec.doctype.exam_assessment_plan.exam_assessment_plan.get_assessment_criteria_detail',
			args: {
				course:d.course,
				criteria:frm.doc.assessment_criteria
			},
			callback: function(r) {
				if (r.message){
					d.total_marks=r.message['total_marks']
					d.total_credit=r.message['credits']
					d.passing_marks=r.message['passing_marks']
					refresh_field("total_marks", d.name, d.parentfield);
					refresh_field("total_credit", d.name, d.parentfield);
					refresh_field("passing_marks", d.name, d.parentfield);
				}
			}
		});
	}
	
});

