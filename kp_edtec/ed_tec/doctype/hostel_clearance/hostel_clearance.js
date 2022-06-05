// Copyright (c) 2022, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Clearance', {
	setup:function(frm){
		frm.set_query("student", function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.hostel_clearance.hostel_clearance.get_hostel_students',
                filters: {
                    "is_hosteller":1
                }
            };
        });
	},
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_hostel_details",
				callback: function(r) { 
					frm.set_value("building",r.message["building"])
					frm.set_value("hostel_room",r.message["to_room"])
					frm.set_value("floor",r.message["floor"])
					frm.set_value("room_type",r.message["room_type"])
				} 
				
			}); 
		}

	}
});
frappe.ui.form.on("Clearance Details", {
	amount:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total = 0;
	frm.doc.clearance_details.forEach(function(d) { total += d.amount; });
	frm.set_value("total", total);
	refresh_field("total");
  },	
});