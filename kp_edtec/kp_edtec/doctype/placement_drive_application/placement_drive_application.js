// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Drive Application', {
	// refresh: function(frm) {

	// }
	setup:function(frm){
		frm.set_query("placement_drive", function() {
			return {
				query:"kp_edtec.kp_edtec.doctype.placement_drive_application.placement_drive_application.get_placement_drive",
				filters: {
					"docstatus": 1,
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("current_semester", function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
	},
	student:function(frm){
		if(frm.doc.student){
			frappe.model.with_doc("Student", frm.doc.student, function() {
                var tabletransfer= frappe.model.get_doc("Student", frm.doc.student)
                frm.clear_table("educational_details");
                $.each(tabletransfer.education_details, function(index, row){
                    var d = frm.add_child("educational_details");
                    d.qualification = row.qualification;
                    d.institute = row.institute;
                    d.board = row.board;
                    d.score = row.score;
					d.percentage = row.percentage;
                    d.year_of_completion = row.year_of_completion;
                    frm.refresh_field("educational_details");
                });
                $.each(tabletransfer.current_education, function(index, row){
                    frm.doc.programs = row.programs;
                    frm.doc.current_semester = row.semesters;
                    frm.refresh_field("programs");
                    frm.refresh_field("current_semester");
                });
            });
        }
	},
	placement_drive:function(frm){
		if(frm.doc.placement_drive){
			frappe.db.get_value("Placement Drive", {'name':frm.doc.placement_drive, "docstatus":1},'eligibility_criteria', resp => {
				frm.set_value("eligibility_details",resp.eligibility_criteria)
			})
			frm.refresh_field("eligibility_details");
		}
	},
	status:function(frm){
		if(frm.doc.status){
			frappe.call({
				method: "kp_edtec.kp_edtec.notification.custom_notification.placement_drive_application_submit",
                args:{
                	'doc':frm.doc
                },
				callback: function(r) { 
					if(r.message){
						frappe.msgprint("Mail sent to student")
					}
				} 
			});
		}
	}
});
