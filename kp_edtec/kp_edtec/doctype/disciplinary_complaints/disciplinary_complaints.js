// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Disciplinary Complaints', {
	refresh:function(frm){
		if (frm.doc.docstatus==1){
			frm.add_custom_button(__("Mentor Mentee Communication"), function() {
				frappe.model.open_mapped_doc({
					method: "kp_edtec.kp_edtec.doctype.disciplinary_complaints.disciplinary_complaints.create_mentor_mentee_communication",
					frm: frm
				})
			}, __('Create'));
		}

		frappe.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Disciplinary Complaints' }

		frm.toggle_display(['contact_html'], !frm.doc.__islocal);

		if (frm.doc.__islocal) {
			frappe.contacts.clear_address_and_contact(frm);
		}
		else {
			frappe.contacts.render_address_and_contact(frm);
		}
		
	},
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_student_details",
				callback: function(r) { 
					frm.refresh()
				} 
			});
		}

	}
});
