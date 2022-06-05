// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Photocopy Application', {
	setup:function(frm){
		frm.set_query("exam_declaration", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.photocopy_application.photocopy_application.get_exam_declaration',
				filters: {
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("post_exam_declaration", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.photocopy_application.photocopy_application.get_post_exam_declaration',
				filters: {
					"student":frm.doc.student,
					"exam_declaration":frm.doc.exam_declaration
				}
			};
		});
		frm.set_query("course","photocopy_item", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.photocopy_application.photocopy_application.get_courses',
				filters: {
					"exam_declaration":frm.doc.exam_declaration,
					"post_exam_declaration":frm.doc.post_exam_declaration
				}
			};
		});
	},
	student: function(frm) {
		frappe.db.get_value("Student",{"name":frm.doc.student},['first_name','last_name'])
		.then(({ message }) => {
			if(message.first_name && message.last_name){
            frm.set_value('student_name',message.first_name +" "+ message.last_name);
			}
			if(message.first_name && !message.last_name){
				frm.set_value('student_name',message.first_name);
				}
				
        });
		if(!frm.doc.student){
			frm.set_value('student_name',"");
		}


	},
	refresh:function(frm){
		if(frm.doc.post_exam_declaration){
			frappe.db.get_value("Post Exam Declaration",{"name":frm.doc.post_exam_declaration},'fees_applicable')
			.then(({ message }) => {
				if(message.fees_applicable == "YES" && !cur_frm.doc.__islocal && !frappe.user.has_role(["Student"])){
					frm.add_custom_button('Fees', () => {

						frappe.model.open_mapped_doc({
							method: "kp_edtec.ed_tec.doctype.photocopy_application.photocopy_application.make_fees",
							frm: me.frm

						})
				
						},
						__('Make')
						)	

				}


			});
		}
			frm.add_custom_button('Reevaluation Application', () => {

						frappe.model.open_mapped_doc({
							method: "kp_edtec.ed_tec.doctype.photocopy_application.photocopy_application.make_reevaluation_application",
							frm: me.frm

						})
				
						},
						__('Make')
						)	
			if(frm.doc.post_exam_declaration && frm.doc.__islocal){
					frappe.call({
						method: "kp_edtec.ed_tec.doctype.photocopy_application.photocopy_application.get_amount",
						args: {
							"post_exam":frm.doc.post_exam_declaration
							
						},
						callback: function(r) {
						
								frm.set_value('total_fees',r.message);				
							}
				
						
				});
					
			}

		
		
	},
	post_exam_declaration:function(frm){
		if(frm.doc.post_exam_declaration){
			frappe.call({
				method: "kp_edtec.ed_tec.doctype.photocopy_application.photocopy_application.get_amount",
				args: {
					"post_exam":frm.doc.post_exam_declaration
					
				},
				callback: function(r) {
				
						frm.set_value('total_fees',r.message);				
					}
		
				
		});
			
	}
	}
});
frappe.ui.form.on("Photocopy Item", "course", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
       if(!d.course){
               d.course_name = ""
               refresh_field("course_name", d.name, d.parentfield);
       }
});
