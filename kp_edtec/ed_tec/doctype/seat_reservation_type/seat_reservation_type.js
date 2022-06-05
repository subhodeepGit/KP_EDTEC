// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Seat Reservation Type', {
	setup: function(frm) {
		frm.set_query("for_criteria","seat_reservations_category_item", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.seat_reservation_type.seat_reservation_type.get_docs',
				filters:{
					"Entries In":"Educations Configurations"
				}
			};
		});
	}
});
