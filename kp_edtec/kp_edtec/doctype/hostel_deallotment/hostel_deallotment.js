// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Deallotment', {
	setup:function(frm){
		frm.set_query("hostel_admission",function(){
			return {
				filters:{
					"student":frm.doc.student,
					"docstatus":1
				}
			}
		})
		frm.set_query("student",function(){
			return {
				query:"kp_edtec.kp_edtec.doctype.hostel_deallotment.hostel_deallotment.get_allotment_students",
				filters:{
					"hostel_allotment":1
				}
			}
		})
	},
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_student_details",
				callback: function(r) { 
					if(r.message){
						frm.set_value("building",r.message["building"])
						frm.set_value("room",r.message["to_room"])
						frm.set_value("room_type",r.message["room_type"])
						frm.set_value("floor",r.message["floor"])
						frm.set_value("hostel_admission",r.message["hostel_admission"])
						frm.set_value("available_beds",r.message["available_beds"])
					}
				} 
			});
		}
	}
});
