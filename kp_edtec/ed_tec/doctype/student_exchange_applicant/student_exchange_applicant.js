// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Exchange Applicant', {
	before_load: function(frm) {
        var df = frappe.meta.get_docfield("Education Qualifications Details","qualification_", frm.doc.name);
        df.hidden = 1
        var df0 = frappe.meta.get_docfield("Education Qualifications Details","qualification", frm.doc.name);
        df0.hidden = 0
        var df1 = frappe.meta.get_docfield("Education Qualifications Details","year_of_completion_", frm.doc.name);
        df1.hidden = 1
        var df11 = frappe.meta.get_docfield("Education Qualifications Details","year_of_completion", frm.doc.name);
        df11.hidden = 0
        var df2 = frappe.meta.get_docfield("Document List","document_name_", frm.doc.name);
        df2.hidden = 1
        var df4 = frappe.meta.get_docfield("Document List","document_name", frm.doc.name);
        df4.hidden = 0
        frm.refresh_fields();
    },
	refresh(frm){
		if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role(["System Manager"])){
            frm.set_df_property('application_status', 'read_only', 1);
        }
		else{
			if (frm.doc.application_status === "Approved" && frm.doc.docstatus === 1) {
				frm.trigger("show_fees_button")
				frm.add_custom_button(__("Enroll"), function() {
					frappe.model.open_mapped_doc({
						method: "kp_edtec.ed_tec.doctype.student_exchange_applicant.student_exchange_applicant.enroll_student",
						frm: frm
					})
				}).addClass("btn-primary");
			}
		}
		let fields_read_only = ["percentage_cgpa"];
		fields_read_only.forEach(function(field) {
			frm.fields_dict.education_qualifications_details.grid.update_docfield_property(
				field, 'read_only', 0
			);
		});

	},
	setup(frm){
		// frm.set_query('student_exchange_program', function(doc) {
		// 	return {
		// 		filters: {
		// 			"application_start":("<",frappe.datetime.get_today())
		// 		}
		// 	};
		// });

		frm.set_query("student_exchange_program", function() {
			return {
				filters: {
					is_active: 1
				}
			};
		});
	
		
	},
	exchange_program(frm){
		frm.trigger("set_student_exchange_program")
	},
	student_category(frm){
		frm.trigger("set_student_exchange_program")
		frm.trigger("get_document_list")
	},
	student_exchange_program(frm){
		frm.trigger("get_document_list")
	},
	set_student_exchange_program(frm){
		if (frm.doc.exchange_program && frm.doc.student_category)
		frappe.call({
            method: "kp_edtec.ed_tec.doctype.student_exchange_applicant.student_exchange_applicant.get_student_exchange_program",
            args: {
                exchange_program: frm.doc.exchange_program,
				student_category : frm.doc.student_category
            },
            callback: function(r) { 
                if (r.message){
                    frm.set_value("student_exchange_program",r.message['name'])
                }
            } 
            
        });  
	},
    show_fees_button(frm){
        if (frm.doc.name && frm.doc.student_exchange_program){
        frappe.call({
            method: "kp_edtec.ed_tec.doctype.student_exchange_applicant.student_exchange_applicant.show_fees_button",
            args: {
                student_exchange_applicant:frm.doc.name,
                exchange_program_declaration:frm.doc.student_exchange_program
            },
            callback: function(r) { 
                if (r.message){
                    frm.add_custom_button(__("Fees"), function() {
                        frappe.model.open_mapped_doc({
                            method: "kp_edtec.ed_tec.doctype.student_exchange_applicant.student_exchange_applicant.create_fees",
                            frm: frm,
                        });
                    })
                }
            } 
        }); 
    }
},
get_document_list(frm){
	frm.set_value("document_list",[])
	if (frm.doc.student_category && frm.doc.student_exchange_program){
		frappe.db.get_doc("Exchange Program Declaration",frm.doc.student_exchange_program).then(( resp1 ) => {
			(resp1.required_documents).forEach((  exchange_row ) => {
				if (frm.doc.student_category==exchange_row.student_category){
					frappe.db.get_doc("Documents Template",exchange_row.document_type).then(( resp2 ) => {
						(resp2.documents_required).forEach((  template_row ) => {
							var d=frm.add_child("document_list");
							d.document_name=template_row.document_name;
							d.mandatory=template_row.mandatory
							frm.refresh_field("document_list")
						})
					})
				}
			})
		});
	}
}

});
