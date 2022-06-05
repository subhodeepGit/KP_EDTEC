// Copyright (c) 2022, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cummulative Marksheet Tool', {
	refresh:function(frm){
		if (!frm.doc.__islocal){
			frm.add_custom_button(__('Create Cummulative Marksheet'), function() {
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
		frm.clear_table("cummulative_marksheet_student");
		frappe.call({
			method: "kp_edtec.ed_tec.doctype.cummulative_marksheet_tool.cummulative_marksheet_tool.get_students",
			args: {
				programs: frm.doc.programs,
				// semester: frm.doc.semester,
				academic_term: frm.doc.academic_term
				// academic_term: frm.doc.academic_term
			},
			// $.each(r.message, function(i, d) {
			// 	var s = frm.add_child('students');
			// 	s.student = d.student;
				// s.student_name = d.student_name;
			callback: function(r) { 
				
				(r.message).forEach(element => {
					// if(in_list(student_list, element.student)) {
					var row = frm.add_child("cummulative_marksheet_student")
					row.student=element.student
					row.student_name=element.student_name
					row.completion_status=element.completion_status
					// if (d.active === 0) {
					// 	s.active = 0;
					// }
					// }
				});
				frm.refresh_field("cummulative_marksheet_student")
				frm.save();
				frm.set_value("total_enrolled_student",(r.message).length)
			} 
			
		});  
	}

});
