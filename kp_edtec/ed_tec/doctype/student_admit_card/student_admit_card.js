// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Admit Card', {
	refresh(frm){
		if (!frappe.boot.desk_settings.form_sidebar) {
			cur_page.page.page.add_action_icon("printer", function() {
				cur_frm.print_doc();
			}, '', __("Print"));
		}
	},
	setup:function(frm){
		frm.trigger("filters")
	},
	student_roll_no(frm){
		frappe.db.get_value("Student", {'name':frm.doc.student_roll_no},'title', resp => {
            frm.set_value('student_name', resp.title)
        })
        frm.trigger("filters")
        frm.clear_table("courses");

        frm.trigger("get_courses")
	},
	current_program: function(frm) {
		frm.trigger("get_courses")
	},
	academic_year: function(frm) {
		frm.trigger("get_courses")
	},
	academic_term: function(frm) {
		frm.trigger("get_courses")
	},
	registration_no :function(frm){
		frm.trigger("get_courses")	
	},
	filters: function(frm) {
		frm.set_query("current_program", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.fees.get_progarms',
				filters: {
					"student":frm.doc.student_roll_no
				}
			};
		});
		frm.set_query("current_semester", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.fees.get_sem',
				filters: {
					"student":frm.doc.student_roll_no
				}
			};
		});
		frm.set_query("courses","courses", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.student_admit_card.student_admit_card.get_courses',
				filters: {
					"program":frm.doc.current_semester
				}
			};
		});
		frm.set_query("registration_no", function() {
			return {
				filters: {
					"docstatus":1
				}
			};
		});
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year
				}
			};
		});
	},
	get_courses: function(frm){
		if (frm.doc.current_program && frm.doc.student_roll_no && frm.doc.academic_year && frm.doc.academic_term){
			frappe.call({
				method: "kp_edtec.ed_tec.doctype.student_admit_card.student_admit_card.get_exam_details",
				args: {
					program:frm.doc.current_program,
					semester:frm.doc.current_semester,
					academic_year:frm.doc.academic_year,
					academic_term:frm.doc.academic_term,
					student:frm.doc.student_roll_no
				},
				callback: function(r) { 
					if (r.message){
						frm.clear_table("courses");
						(r.message).forEach(element => {
							var c = frm.add_child("courses")
                            c.courses=element.courses;
                            c.course_code = element.course_code;
                            c.course_name = element.course_name;
                            c.semester = element.semester;
							c.examination_date=element.examination_date;
							c.from_time=element.from_time;
							c.to_time=element.to_time;
							c.total_duration_in_hours=element.total_duration_in_hours;
						})
						frm.refresh_field("courses")
					}
				} 
				
			});    
	}
	},
});
