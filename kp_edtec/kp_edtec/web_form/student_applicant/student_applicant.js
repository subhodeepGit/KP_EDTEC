frappe.ready(function() {
	frappe.web_form.after_load = () => {
		frappe.web_form.set_df_property('program_priority', 'hidden', 1);
	    frappe.web_form.on('academic_year', (field, value) => {
			if(value){
				frappe.call({
					method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_academic_term",
					args:{
                        'academic_year':value
					},
					callback: function(r) {
					    frappe.web_form.fields_dict.academic_term._data = create_dict(r.message);
					}
				});	
			}	
		});
		frappe.web_form.on('tribe', (field, value) => {
			if(value){
				frappe.call({
					method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_sub_tribe",
					args:{
						'tribe':value
					},
					callback: function(r) {
						$.each(r.message || [], function(i, d) {
							if (d.tribe == value){
								$('[data-fieldname="tribe_name"]').val(d.tribe_name);
							}
						});
						frappe.web_form.fields_dict.sub_tribe._data = create_dict(r.message);
					}
				});
			}
		});
		frappe.web_form.on('sub_tribe', (field, value) => {
			if(value){
				frappe.call({
					method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_sub_tribe_name",
					args:{
						'name':value
					},
					callback: function(r) {
					    $('[data-fieldname="sub_tribe_name"]').val(r.message);
					}
				});
			}
		});
		frappe.web_form.on('states', (field, value) => {
			if(value){
				frappe.call({
					method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_phone_code",
					args:{
						'states':value
					},
					callback: function(r) {
					    $('[data-fieldname="country_code"]').val(r.message);
					}
				});
			}
		});
		frappe.web_form.on('student_category', (field, value) => {
			if(value){
				frappe.call({
					method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_document_list",
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
			method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_department",
			callback: function(r) {
			    frappe.web_form.fields_dict.department._data = create_dict(r.message);
			}
		});
		frappe.call({
			method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_qualification_list",
            callback: function(r) {
            	frappe.web_form.fields_dict.education_qualifications_details.grid.fields_map.qualification_.options = r.message.qual;
                frappe.web_form.fields_dict.education_qualifications_details.grid.fields_map.year_of_completion_.options = r.message.acadmic;
            }
        });
        
		frappe.web_form.on('program_grade', (field, value) => {
			filter_program_choice()
		});
		frappe.web_form.on('department', (field, value) => {
			filter_program_choice()
		});
		frappe.web_form.on('program_choice_1', (field, value) => {
			if(value){
				frappe.call({
					method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_counselling_structure",
					args:{
						'programs':value
					},
					callback: function(r) {
					    $('[data-fieldname="counselling_structure"]').val(r.message);
					}
				});
			}
		});
	}
	let filter_program_choice = function(){
		if(frappe.web_form.get_value('department') && frappe.web_form.get_value('program_grade')){
			frappe.call({
				method: "kp_edtec.kp_edtec.web_form.student_applicant.student_applicant.get_programs_list",
				args:{
						"department":frappe.web_form.get_value('department'),
		                "program_grade": frappe.web_form.get_value('program_grade')
				},
				callback: function(r) {
					var result = create_dict(r.message);
				    frappe.web_form.fields_dict.program_choice_1._data = result;
				    frappe.web_form.fields_dict.program_choice_2._data = result
				    frappe.web_form.fields_dict.program_choice3._data = result
				    frappe.web_form.fields_dict.program_choice_4._data = result
				    frappe.web_form.fields_dict.program_choice_5._data = result
				    frappe.web_form.fields_dict.program_choice_6._data = result
				}
			});
		}
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

