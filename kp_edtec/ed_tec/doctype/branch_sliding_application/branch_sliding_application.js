// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Branch Sliding Application', {
	refresh(frm){
		if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role('System Manager')){
            frm.set_df_property('status', 'read_only', 1);
        }
		else if (frm.doc.status === "Approved" && frm.doc.docstatus === 1 ) {
            frm.trigger("show_fees_button")
			frm.add_custom_button(__("Enroll"), function() {
				frappe.model.open_mapped_doc({
					method: "kp_edtec.ed_tec.doctype.branch_sliding_application.branch_sliding_application.enroll_student",
					frm: frm
				})
			}).addClass("btn-primary");
        }
	},
	setup(frm){
		frm.set_query("sliding_in_program", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.branch_sliding_application.branch_sliding_application.get_sliding_in_progam',
				filters: {
					"branch_sliding_declaration":frm.doc.branch_sliding_declaration,
				}
			};
		});
	},
	student(frm){
		if (frm.doc.student){
			frappe.call({
				method: "kp_edtec.ed_tec.doctype.branch_sliding_application.branch_sliding_application.get_student_details",
				args: {
					student: frm.doc.student,
				},
				callback: function(r) { 
					if (r.message){
						frm.set_value("current_program",r.message['programs'])
						frm.set_value("academic_year",r.message['academic_year'])
						frm.set_value("branch_sliding_declaration",r.message['declaration'])
					}
				} 
				
			});    
	}
	},
	sliding_in_program(frm){
		// if (!frm.doc.branch_sliding_declaration){
		// 	frappe.throw("please fill <b>Branch Change Declaration</b> First")
		// }
		// if (!frm.doc.sliding_in_program){
		// 	frappe.throw("please fill <b>Sliding in Program</b> First")
		// }
		if (frm.doc.branch_sliding_declaration && frm.doc.sliding_in_program){
			frappe.call({
				method: "kp_edtec.ed_tec.doctype.branch_sliding_application.branch_sliding_application.get_declaration_details",
				args: {
					branch_declaration:frm.doc.branch_sliding_declaration,
					sliding_in_program:frm.doc.sliding_in_program
				},
				callback: function(r) { 
					if (r.message){
						frm.set_value("sliding_in_semester",r.message)
					}
				} 
				
			});    
		}
	},
	branch_sliding_declaration(frm){
		frm.set_value("sliding_in_program",'')
	}
});
