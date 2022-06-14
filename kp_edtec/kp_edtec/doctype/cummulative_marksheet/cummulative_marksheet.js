// Copyright (c) 2022, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cummulative Marksheet', {
	student(frm){
		if (frm.doc.student) {
			frappe.call({
				method: 'get_student_details',
				doc:frm.doc,
				callback: function(r) {
					if (r.message) {
						// frm.doc.course_assessment_credit = [];
						// $.each(r.message, function(i, d) {
						// 	var row = frm.add_child("course_assessment_credit")
						// 	row.course = d.courses;
						// 	row.credit=d.total;
						// });
					}
					frm.refresh();
					refresh_field('cummulative_courses_item');
				}
			});
		}
	}
});
