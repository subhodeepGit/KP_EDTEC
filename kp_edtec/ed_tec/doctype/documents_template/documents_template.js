// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Documents Template', {
	student_category: function(frm) {
		if (frm.doc.student_category){
			frappe.db.get_doc("Student Category",frm.doc.student_category).then(( resp ) => {
				frm.clear_table("documents_required");
				(resp.admission_document_list).forEach(( document_row ) => {
					var row=frm.add_child("documents_required");
					row.document_name=document_row.document_name
					row.mandatory=document_row.mandatory
					row.is_available=document_row.is_available
					frm.refresh_field("documents_required");
				})
			});
		}
	}
});
