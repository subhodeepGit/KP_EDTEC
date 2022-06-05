// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Company', {
	refresh: function(frm) {
		frappe.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Placement Company' }

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if (frm.doc.__islocal) {
			frappe.contacts.clear_address_and_contact(frm);
		}
		else {
			frappe.contacts.render_address_and_contact(frm);
		}
		frm.add_custom_button(__("Placement Drive"), function() {
			frappe.model.open_mapped_doc({
				method: "kp_edtec.ed_tec.doctype.placement_company.placement_company.create_placement_drive",
				frm: frm,
			});
		}, __('Create'))
	},
	setup(frm) {
        frm.set_query("department","belong_to_department", function() {
			return {
				filters: {
					"is_stream":0
				}
			};
		});
    }
});
