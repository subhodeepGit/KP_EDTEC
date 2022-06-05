// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Leave Application', {
	setup:function(frm){
		frm.set_query("student", function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.hostel_leave_application.hostel_leave_application.get_hosteler_students',
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
					frm.set_value("hostel_building",r.message["building"])
					frm.set_value("room_no",r.message["to_room"])
				} 
				
			}); 
		}

	}
});
