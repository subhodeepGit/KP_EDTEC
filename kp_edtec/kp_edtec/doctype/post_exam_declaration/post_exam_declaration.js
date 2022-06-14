// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Post Exam Declaration', {
	setup: function(frm) {
		frm.set_query('fee_structure', 'fee_structure', function() {
		    return {
				query: 'kp_edtec.kp_edtec.doctype.post_exam_declaration.post_exam_declaration.get_fee_structure',
				filters: {
					"declaration":frm.doc.exam_declaration
				}
			};
		});
	},
	before_save:function(frm){
		if(frm.doc.start_date && frm.doc.end_date && frm.doc.start_date > frm.doc.end_date){
				frappe.throw("End Date should be greater than start date");
		}

	}
});
