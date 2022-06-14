// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mentor', {
	instructor: function(frm) {
		if (frm.doc.instructor){
			frappe.call({
				method: "kp_edtec.kp_edtec.doctype.mentor.mentor.get_instructor_data",
				args: {
					instructor: frm.doc.instructor
				},
				callback: function(r) {
					if(r.message){
					    if (r.message.user_id){
							frm.doc.user = r.message.user_id
							frm.refresh_fields("user");
						}
						else{
							frappe.msgprint(__("User not exist. Please click on create user button."));
						}
						if (r.message.company_email){
							frm.doc.email_id = r.message.company_email
							frm.refresh_fields("email_id");
						}
						else if (r.message.personal_email){
							frm.doc.email_id = r.message.personal_email
							frm.refresh_fields("email_id");
						}
					}
					else{
						frappe.msgprint(__("User not exist. Please enter email id and click on create user button"));
					}
				}
			});
		}
	},
	create_user: function(frm) {
		frm.set_df_property('email_id', 'reqd', 1);
		frappe.db.get_value("User", {'name':frm.doc.email_id},'name', resp => {
            frm.set_value('user', resp.name)
        })
		if (frm.doc.email_id && !frm.doc.user){
			frappe.call({
				method: "kp_edtec.kp_edtec.doctype.mentor.mentor.create_user",
				args: {
					doc: frm.doc
				},
				callback: function(r) {
					if(r.message){
						frm.doc.user = frm.doc.email_id
					}
				}
			});
		}
		else{
			frappe.msgprint(__("Please enter email id."));
		}
	}
});
