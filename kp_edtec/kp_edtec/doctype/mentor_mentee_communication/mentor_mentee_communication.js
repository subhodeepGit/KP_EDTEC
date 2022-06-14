// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mentor Mentee Communication', {
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) { 
					if(r.message){
						if (r.message['mentor']){
							frm.set_value("mentor",r.message['mentor'])
						}
						if (r.message['mentor_name']){
							frm.set_value("mentor_name",r.message['mentor_name'])
						}
						frm.set_value("programs",r.message['programs'])
					}
				} 
			}); 
		}
	},
	setup: function(frm){
		if(frm.doc.mentor){
			frm.set_query("student", function() {
				return {
					query: 'kp_edtec.kp_edtec.doctype.mentor_mentee_communication.mentor_mentee_communication.get_students',
					filters: {
						"mentor":frm.doc.mentor
					}
				};
			});
		}
		
	}
});
