// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Exchange Program Declaration', {
	setup(frm){
		frm.set_query("exchange_program", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.exchange_program_declaration.exchange_program_declaration.get_active_exchange_program_declaration',
				filters: {
					is_active: 1
				}
			};
		});
		frm.set_query("semester", function() {
			return {
				filters: {
					"programs":frm.doc.program__to_exchange
				}
			};
		});
		frm.set_query("fee_structure","fee_structure", function(){
            return{
                filters:{
                    "fee_type":"Student Exchange Application Fees",
                    "programs":frm.doc.program__to_exchange,
                    "docstatus":1
                }
            }
        })
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year
				}
			};
		});
		frm.set_query("academic_calendar_template", function() {
			return {
				filters: {
					"programs":frm.doc.program__to_exchange,
					"program":frm.doc.semester
				}
			};
		});

		frm.set_query("document_type","required_documents", function(){
            return{
                filters:{
                    "is_active":1
                }
            }
        })

	}
});
frappe.ui.form.on("Required Documents", "document_type", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    frappe.db.get_value("Documents Template", {'name':d.document_type},'student_category', resp => {
        frappe.model.set_value(cdt, cdn, "student_category", resp.student_category);
    })
});
