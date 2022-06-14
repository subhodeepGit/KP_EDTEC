// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Allotment', {
	setup:function(frm){
		frm.set_query("hostel_admission",function(){
			return {
				filters:{
					"student":frm.doc.student,
					"docstatus":1
				}
			}
		})
		frm.set_query("student", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.hostel_allotment.hostel_allotment.get_hostel_students',
				filters:{
					"hostel_admission":1
				}
			};
		});
		frm.set_query("to_room", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.hostel_allotment.hostel_allotment.get_rooms',
			    filters: {
                    "building":frm.doc.building,
                    "room_type":frm.doc.room_type,
                    "floor":frm.doc.floor,
					"seat_balance":[">=",1],
					"from_room":frm.doc.from_room,
                }
			};
		});
		frm.set_query("building", function() {
			return {
				filters:{
					"disable":0
				}
			};
		});
	},
	to_room:function(frm){
		if (frm.doc.to_room){
			frappe.db.get_value("Hostel Room", {'name':frm.doc.to_room},['building','room_type','floor', 'seat_balance'], resp => {
				frm.set_value("building",resp.building)
				frm.set_value("room_type",resp.room_type)
				frm.set_value("floor",resp.floor)
				frm.set_value("available_beds",resp.seat_balance)
			})
		}
		
	},

	student:function(frm){
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_hostel_details",
				callback: function(r) { 
					frm.refresh();
					frm.trigger("map_existing_details");
				} 
			});
		}
	},
	purpose:function(frm){
		frm.trigger("map_existing_details");
	},
	map_existing_details:function(frm){
		frappe.call({
			doc:frm.doc,
			method: "map_fields_if_shifting",
			callback: function(r) { 
				frm.refresh()
			} 
		});
	}
});
