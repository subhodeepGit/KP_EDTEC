// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Counselling Structure', {
	refresh: function(frm) {
			// frm.add_custom_button(__("Student Admission"), function() {
			// 	frappe.model.open_mapped_doc({
			// 		method: "kp_edtec.kp_edtec.doctype.counselling_structure.counselling_structure.create_student_admission",
			// 		frm: frm,
			// 	});
			// }, __('Create'))
		
	},
	setup: function(frm) {
		var program_list= []
		frm.set_query("fee_structure","counselling_fees", function(){
	        $.each(frm.doc.counselling_programs, function(index, row){
                program_list.push(row.programs);
	        });
	        return{
	            filters:{
	            	"programs":  ['in', program_list],
	            	"docstatus":1,
	                "fee_type":"Counselling Fees"
	            }
	        }
	    });
		frm.fields_dict['counselling_programs'].grid.get_field('programs').get_query = function(doc, cdt, cdn) {
            return {   
                query: 'kp_edtec.kp_edtec.doctype.counselling_structure.counselling_structure.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.department,
                    "program_grade": frm.doc.program_grade
                }
            }
        }
		frm.set_query("document_type","required_documents", function(){
            return{
                filters:{
                    "is_active":1
                }
            }
        })
		frm.set_query("department", function(){
	        return{
	            filters:{
	                "is_group":1,
	                "is_stream": 1
	            }
	        }
	    });
	}
});
frappe.ui.form.on("Required Documents", {
	document_type: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		row.student_category=''
		frm.refresh_field("required_documents");
		if (row.document_type) {
			frappe.db.get_value("Documents Template", {'name':row.document_type},'student_category', resp => {
					row.student_category=resp.student_category
					frm.refresh_field("required_documents");
			})
			
		} 
	},
});