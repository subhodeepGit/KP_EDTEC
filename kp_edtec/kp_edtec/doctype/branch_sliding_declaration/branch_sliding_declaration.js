// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Branch sliding Declaration', {
	setup:function(frm){
		frm.set_query("program","branch_sliding__criteria", function() {
			return {
				query:"kp_edtec.kp_edtec.doctype.branch_sliding_declaration.branch_sliding_declaration.get_programs",
				filters: {
					"Department":"Exist In For Program",
					"programs":frm.doc.for_program
				}
			};
		});
		frm.set_query("semester","branch_sliding__criteria",function(frm, cdt, cdn){
            var d = locals[cdt][cdn];
            return{
            	query:"kp_edtec.kp_edtec.doctype.branch_sliding_declaration.branch_sliding_declaration.get_semesters",
                filters:{
                    "programs":d.program
                }
            }
        })
	}
});
frappe.ui.form.on("Branch Sliding Item", "update_seats", function(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	let dialog = new frappe.ui.Dialog({
	title: __('Update Seats'),
	fields: [
		{
			"label" : "Type",
			"fieldname": "type",
			"fieldtype": "Select",
			"options":"\nAdd Balance\nDeduct Balance",
			"reqd":1
		},
		{
			"label" : "No of Seats",
			"fieldname": "no_of_seats",
			"fieldtype": "Int"
		}
	],
	primary_action: function() {
		var data=dialog.get_values();
		if (data.type=="Add Balance"){
			frappe.model.set_value(cdt, cdn, "total_seats", (d.total_seats || 0)+data.no_of_seats);
			frappe.model.set_value(cdt, cdn, "available_seats", (d.available_seats || 0)+data.no_of_seats);
		}
		else{
			frappe.model.set_value(cdt, cdn, "total_seats", (d.total_seats || 0)-data.no_of_seats);
			frappe.model.set_value(cdt, cdn, "available_seats", (d.available_seats || 0)-data.no_of_seats);
		}
		dialog.hide();
	},
	primary_action_label: __('Update')
	});
	dialog.show();
   
});
