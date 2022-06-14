// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Room', {
	// room_number: function(frm) {
	// 	// console.log("//////////////type_of(room_number)",typeof(frm.doc.room_number))
	// 	// if(frm.doc.room_number)
 //  //       frappe.msgprint(__("Score of <b>Teaching Activity</b> must be less than or equal to <b>50</b>"));
	// }
	setup:function(frm){
       frm.set_query("building",function(){
			return {
				filters:{
					"disable":0
				}
			}
		})
	},
	refresh:function(frm){
		frm.add_custom_button(__("Add Balance"), function() {
			let d = new frappe.ui.Dialog({
			title: __('Add Seat Capacity'),
			fields: [
				{
					"label" : "Add Seat",
					"fieldname": "add_seat",
					"fieldtype": "Int"
				}
			],
			primary_action: function() {
				frm.doc.seat_type = "Add Balance";
                frm.doc.seats = d.get_value("add_seat");
				frappe.call({
					method: "create_allotment_ledger",
					doc: frm.doc,
					callback: function(r) { 
						frm.reload_doc();
					} 
					
				});  
				d.hide();
			},
			primary_action_label: __('Add')
		});
		d.show();
		}, __('Create'))

		frm.add_custom_button(__("Deduct Balance"), function() {
			let d = new frappe.ui.Dialog({
			title: __('Deduct Seat Capacity'),
			fields: [
				{
					"label" : "Deduct Seat",
					"fieldname": "deduct_seat",
					"fieldtype": "Int"
				}
			],
			primary_action: function() {
				frm.doc.seat_type = "Deduct Balance";
                frm.doc.seats = d.get_value("deduct_seat");
				frappe.call({
					method: "create_allotment_ledger",
					doc: frm.doc,
					callback: function(r) { 
						frm.reload_doc();
					} 
					
				});  
				d.hide();
			},
			primary_action_label: __('Deduct')
		});
		d.show();
		}, __('Create'))
	}
});
