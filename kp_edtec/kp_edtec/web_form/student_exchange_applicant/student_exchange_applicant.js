frappe.ready(function() {
	// bind events here
	
	frappe.web_form.after_load = () => {
        frappe.web_form.on('student_exchange_program', (field, value) => {
			if(value){
				frappe.call({
					method: "frappe.client.get",
					args:{
		                doctype: "Exchange Program Declaration",
		                filters: { name: value}
					},
					callback: function(r) {
						$('[data-fieldname="academic_year"]').val(r.message.academic_year);
					    $('[data-fieldname="academic_term"]').val(r.message.academic_term);
					    $('[data-fieldname="exchange_program"]').val(r.message.program__to_exchange);
					}
				});
			}
		});
		frappe.web_form.on('student_category', (field, value) => {
			if(value){
				frappe.call({
					method: "kp_edtec.kp_edtec.web_form.student_exchange_applicant.student_exchange_applicant.get_document_list",
		            args:{
						'student_category':value
					},
		            callback: function(r) {
		            	frappe.web_form.fields_dict.document_list.grid.fields_map.document_name_.options = r.message;
		            }
		        });
			}
			else{
				frappe.msgprint('Please select student category first.');
			}
		});
		frappe.call({
			method: "kp_edtec.kp_edtec.web_form.student_exchange_applicant.student_exchange_applicant.get_guardian_list",
            callback: function(r) {
            	frappe.web_form.fields_dict.guardians.grid.fields_map.guardian_.options = r.message;
            }
        });
        frappe.call({
			method: "kp_edtec.kp_edtec.web_form.student_exchange_applicant.student_exchange_applicant.get_qualification_list",
            callback: function(r) {
            	frappe.web_form.fields_dict.education_qualifications_details.grid.fields_map.qualification_.options = r.message.qual;
                frappe.web_form.fields_dict.education_qualifications_details.grid.fields_map.year_of_completion_.options = r.message.acadmic;
            }
        });

		frappe.call({
			method: "frappe.client.get_list",
			args:{
                doctype: "Exchange Program Declaration",
				order_by: "name",
				fields: ["name"]
			},
			callback: function(r) {
			    frappe.web_form.fields_dict.student_exchange_program._data = create_dict(r.message);
			}
		});
	}
	let create_dict = function(r){
		var dict = [];
		 $.each(r || [], function(i, d) {
			dict.push({
			   'label': d.name,
			   'value': d.name
			});
		});
		return dict 
	}
})