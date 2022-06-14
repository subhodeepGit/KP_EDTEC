// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Disciplinary Complain', {
	refresh: function(frm) {
		if (!frm.doc.__islocal){
			frm.add_custom_button("Mentor Mentee Communication", () => {
				let data = {}
				data.student=frm.doc.student
				data.student_name=frm.doc.student_name
				data.date=frm.doc.date
				data.description=frm.doc.description
				data.student_disciplinary_complain=frm.doc.name
				data.mentor=frm.doc.mentor
				frappe.new_doc("Mentor Mentee Communication", data)
			},__('Create'));
		}
	}
});
