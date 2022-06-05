// Copyright (c) 2022, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transfer Certificate', {
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) {
				    frm.set_value("date",frappe.datetime.get_today()) 
					if(r.message){
						if (r.message['enrollment_dte']){
							frm.set_value("date_of_admission_as_in_the_admission_register",r.message['enrollment_dte'])
						}
						if (r.message['class']){
							frm.set_value("class_in_which_studying",r.message['class'])
						}
						if (r.message['class']){
							frm.set_value("subjects_taken",r.message['class'])
						}
					}
				} 
			}); 
		}
	}
});