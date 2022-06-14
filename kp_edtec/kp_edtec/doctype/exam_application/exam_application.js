// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Exam Application', {
	refresh: function(frm) {
		if (frm.doc.docstatus==1 && !frappe.user.has_role(["Student"]) ){
			frm.add_custom_button(__('Fees'), function() {
				frappe.model.open_mapped_doc({
					method: "kp_edtec.kp_edtec.doctype.exam_application.exam_application.make_fees",
					frm: frm,
				});
			}, __('Create'))
		}
		frappe.db.get_single_value('Educations Configurations', 'exam_fee_applicable').then(val => {
			if (!val) {
					frm.set_df_property('examination_fees_section', 'hidden', 1);
			}
		})
	},
	setup:function(frm){
		frm.set_query("exam_declaration", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.exam_application.exam_application.get_exam_declaration',
				filters: {
					"student":frm.doc.student,
					"disabled":0,
					"is_application_required":1,
					"application_form_start_date":["<=",frm.doc.date],
					"application_form_end_date":[">=",frm.doc.date],
				}
			};
		});	
	},
	get_courses:function(frm){
		frm.clear_table("exam_application_courses");
        if (frm.doc.exam_declaration&&frm.doc.student){
                frappe.call({
                    method: "kp_edtec.kp_edtec.doctype.exam_application.exam_application.get_courses_from_declaration",
                    args: {
                        exam_declaration: cur_frm.doc.exam_declaration,
						student:frm.doc.student
                    },
                    callback: function(r) { 
						if(r.message){
							var duplicate=[];
							(r.message).forEach(element => {
								if (!duplicate.includes(element)){
									duplicate.push(element)
									var c = frm.add_child("exam_application_courses")
									c.course = element.name
				                    c.course_code = element.course_code
			                        c.course_name = element.course_name
			                        c.semester = element.semester
								}
							});
						}
                        cur_frm.refresh_field("exam_application_courses")
                    } 
                });    
        }
	},
	student(frm){
		if (!frm.doc.student){
            frm.set_value('student_name', '')
            frm.set_value('exam_declaration', '')
            frm.set_value('current_program', '')
        }

		// if (frm.doc.student){
		// 	frappe.call({
		// 		method: "kp_edtec.kp_edtec.doctype.student_applicant.get_student_applicant_details",
		// 		args: {
		// 			student:frm.doc.student,
		// 		},
		// 		callback: function(r) { 
		// 			if (r.message){
		// 				frm.set_value("program_academic_year",r.message['academic_year'])
		// 				frm.set_value("academic_term",r.message['academic_term'])
		// 				frm.set_value("academic_term",r.message['academic_term'])
		// 				frm.set_value("current_program",r.message['programs_'])
		// 				frm.set_value("current_semester",r.message['program'])
		// 			}
		// 		} 
				
		// 	}); 
		// }
		frm.trigger("get_courses")
		if(frm.doc.student && frm.doc.exam_declaration){
			frappe.call({
				method: "kp_edtec.kp_edtec.doctype.exam_application.exam_application.get_declaration_details",
				args: {
					declaration:frm.doc.exam_declaration,
					student:frm.doc.student
				},
				callback: function(r) { 
					if (r.message){
						frm.set_value("exam_fee",r.message.exam_fees)
					}
				} 
				
			});

		}
		frm.trigger("get_fees_amount")
	},
	exam_declaration(frm){
		frm.trigger("get_fees_amount")
		frm.trigger("get_courses")
		frm.clear_table("semesters");
		if(frm.doc.student && frm.doc.exam_declaration){
			frappe.call({
				method: "kp_edtec.kp_edtec.doctype.exam_application.exam_application.get_declaration_details",
				args: {
					declaration:frm.doc.exam_declaration,
					student:frm.doc.student
				},
				callback: function(r) { 
					if (r.message){
						frm.set_value("exam_fee",r.message.exam_fees);
						(r.message.semesters).forEach(element => {
							var row = frm.add_child("semesters")
							row.semester=element.semester
						});
						frm.refresh_field("semesters")
					}
				} 
				
			});

		}


	},
	get_fees_amount(frm){
		if (frm.doc.student && frm.doc.exam_declaration){
			frappe.call({
				method: "kp_edtec.kp_edtec.doctype.exam_application.exam_application.get_declaration_details",
				args: {
					declaration:frm.doc.exam_declaration,
					student:frm.doc.student
				},
				callback: function(r) { 
					if (r.message){
						frm.set_value("exam_fee",r.message.exam_fees)
					}
				} 
				
			});  
		}
	}
});
