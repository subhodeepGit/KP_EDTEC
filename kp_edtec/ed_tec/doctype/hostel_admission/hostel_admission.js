// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hostel Admission', {
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) { 
					frm.refresh()
				} 
				
			}); 
		}
	},
    refresh: function(frm) {
        if(frm.doc.docstatus == 1 && (frm.doc.hostel_fee_structure || frm.doc.mess_fee_structure)){
            frm.add_custom_button(__("Fees"), function() {
                // frappe.model.open_mapped_doc({
                //     method: "ed_tec.ed_tec.doctype.hostel_admission.hostel_admission.create_fees",
                //     frm: frm,
                // });
                frm.trigger("fees_dialog");
            }, __('Create'))
        }
		if (!frm.doc.__islocal && frm.doc.docstatus==1){
			frm.add_custom_button("Hostel Allotment", () => {
				let data = {}
				data.student=frm.doc.student
				data.student_name=frm.doc.student_name
				data.date=frm.doc.date
				data.hostel_admission=frm.doc.name
				frappe.new_doc("Hostel Allotment", data)
			},__('Create'));
			frm.add_custom_button("Hostel Deallotment", () => {
				let data = {}
				data.student=frm.doc.student
				data.student_name=frm.doc.student_name
				data.date=frm.doc.date
				data.hostel_admission=frm.doc.name
				frappe.new_doc("Hostel Deallotment", data)
			},__('Create'));
		}
    },
    terms_template: function(frm) {
         frappe.db.get_value("Terms and Conditions", {'name':frm.doc.terms_template, 'hostel':1},'terms', resp => {
            frm.set_value('description', resp.terms)
        })
    },
    hostel_type: function(frm) {
         frappe.db.get_value("Room Type", {'name':frm.doc.hostel_type},['fees_structure','total_amount'], resp => {
            frm.set_value('hostel_fee_structure', resp.fees_structure)
            frm.set_value('amount', resp.total_amount)
        })
    }, 
    setup:function(frm) {
        frm.set_query("guardian","guardian_list", function() {
            return {
                filters: {
                    "student":frm.doc.student
                }
            };
        });
        frm.set_query("hostel_fee_structure", function() {
            return {
                filters: {
                    "fee_type":["in", ["Hostel Fees", "Mess Fees"]]
                }
            };
        });
    },
    fees_dialog:function(frm){
       var  fee_type_options="";
       if (frm.doc.hostel_fee_structure){
           fee_type_options+=("\nHostel Fees")
       }
       if (frm.doc.mess_fee_structure){
        fee_type_options+=("\nMess Fees")
        }
        var dialog = new frappe.ui.Dialog({
			title: __('Create Fees'),
            fields: [
				{
					"label" : "Select Fees Type",
					"fieldname": "fee_type",
					"fieldtype": "Select",
					"options":fee_type_options,
					"reqd":1,
					onchange: function() {
						var fee_type=dialog.get_value('fee_type');
						dialog.set_value("fee_structure","");
						if (fee_type){
							dialog.set_value("fee_structure",frm.doc.hostel_fee_structure);
							if (fee_type=="Mess Fees"){
								dialog.set_value("fee_structure",frm.doc.mess_fee_structure);
							}
						}
					}
				},
				{
					"fieldname": "column_break_1",
					"fieldtype": "Column Break"
				},
				{
					"label" : "Fee Structure",
					"fieldname": "fee_structure",
					"fieldtype": "Link",
                    "read_only":1
				},
				{
					"fieldname": "section_break_1",
					"fieldtype": "Section Break"
				},
                {
					"label" : "From Date",
					"fieldname": "from_date",
					"fieldtype": "Date",
                    "reqd":1
				},
				{
					"fieldname": "column_break_2",
					"fieldtype": "Column Break"
				},
                {
					"label" : "To Date",
					"fieldname": "to_date",
					"fieldtype": "Date",
                    "reqd":1
				}
			],
			primary_action: function() {
				var values=dialog.get_values()
                if (values["from_date"]>values["to_date"]){
                    frappe.throw("From Date Cann't be Greater than To Date");
                }
				frappe.call({
					method:"kp_edtec.ed_tec.doctype.hostel_admission.hostel_admission.create_fees",
					args: {
						source_name:frm.doc.name,
						dialog_value:values
					}
			  })
				dialog.hide();
			},
			primary_action_label: __('Add')
		});
		dialog.show();
    }
});
