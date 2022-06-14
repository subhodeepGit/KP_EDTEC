// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Result Declaration', {
	setup: function(frm) {
		frm.set_query('semester', function(doc) {
			return {
				filters: {
					"programs":frm.doc.programs
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
	refresh:function(frm){
		if (!frm.doc.__islocal){
			frm.add_custom_button(__('Create Exam Assessment Result'), function() {
				frappe.call({
					method: 'make_exam_assessment_result',
					doc: frm.doc,
					callback: function() {
						frm.refresh();
					}
				});
			}).addClass('btn-primary');;
		}
		
	},
	onload:function(frm){
		frappe.realtime.on('final_result_declaration_progress', function(data) {
			if (data.reload && data.reload === 1) {
				frm.reload_doc();
			}
			if (data.progress && frm.doc.result_creation_status === 'In Process' && data.current && data.total) {
				cur_frm.dashboard.show_progress('Result Creation Status',data.progress+'%',__('Created Exam Assessment Result {0} of {1}', [data.current,data.total]))
			}
		});
	},
	get_students:function(frm){
		frm.clear_table("result_declaration_student");
		frappe.call({
			method: "kp_edtec.kp_edtec.doctype.final_result_declaration.final_result_declaration.get_enroll_students",
			args: {
				programs: frm.doc.programs,
				semester: frm.doc.semester,
				academic_year: frm.doc.academic_year,
				academic_term: frm.doc.academic_term
			},
			callback: function(r) { 
				(r.message).forEach(element => {
					var row = frm.add_child("result_declaration_student")
					row.student=element.name
					row.student_name=element.title
					row.completion_status=element.completion_status
				});
				frm.refresh_field("result_declaration_student")
				frm.set_value("total_enrolled_student",(r.message).length)
			} 
			
		});  
	}
});
