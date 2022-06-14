// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reevaluation Application', {
	setup:function(frm){
		frm.set_query("exam_declaration", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.photocopy_application.photocopy_application.get_exam_declaration',
				filters: {
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("course","photocopy_item", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.photocopy_application.photocopy_application.get_courses',
				filters: {
					"exam_declaration":frm.doc.exam_declaration,
				}
			};
		});
		frm.set_query("post_exam_declaration", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.photocopy_application.photocopy_application.get_post_exam_declaration',
				filters: {
					"student":frm.doc.student
				}
			};
		});
	},
	refresh:function(frm){
		if(frm.doc.post_exam_declaration && frm.doc.__islocal){
			frappe.call({
				method: "kp_edtec.kp_edtec.doctype.photocopy_application.photocopy_application.get_amount",
				args: {
					"post_exam":frm.doc.post_exam_declaration
					
				},
				callback: function(r) {
				
						frm.set_value('total_fees_payable',r.message);				
					}
		
				
		});
		// frappe.db.get_value("Post Exam Declaration",{"name":frm.doc.post_exam_declaration},'fees_applicable')
		// .then(({ message }) => {
		// 	if(message.fees_applicable == "YES"){
		// 		frm.add_custom_button('Fees', () => {

		// 			frappe.model.open_mapped_doc({
		// 				method: "kp_edtec.kp_edtec.doctype.reevaluation_application.reevaluation_application.make_fees",
		// 				frm: me.frm

		// 			})
			
		// 			},
		// 			__('Make')
		// 			)	

		// 	}


		// });
			
	}
	}
	
});
