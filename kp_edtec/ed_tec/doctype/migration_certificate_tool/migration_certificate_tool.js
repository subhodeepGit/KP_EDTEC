// Copyright (c) 2022, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Migration Certificate Tool', {

	refresh:function(frm){
		if (!frm.doc.__islocal){
			frm.add_custom_button(__('Create Migration Certificate'), function() {
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
	get_students:function(frm){
		frm.clear_table("migration_certificate_student");
		frappe.call({
			method: "kp_edtec.ed_tec.doctype.migration_certificate_tool.migration_certificate_tool.get_students",
			args: {
				programs: frm.doc.programs,
				academic_term: frm.doc.academic_term
			},
			callback: function(r) { 
				
				(r.message).forEach(element => {
					var row = frm.add_child("migration_certificate_student")
					row.student=element.student
					row.student_name=element.student_name
					row.completion_status=element.completion_status
				});
				frm.refresh_field("migration_certificate_student")
				frm.save();
				frm.set_value("total_enrolled_student",(r.message).length)
			} 
			
		});  
	}

});
