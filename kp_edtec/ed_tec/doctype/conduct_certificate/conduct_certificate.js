// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conduct Certificate', {
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) { 
					frm.set_value("date",frappe.datetime.get_today())
					if(r.message){
						if (r.message['academic_year']){
							frm.set_value("academic_year",r.message['academic_year'])
						}
						if (r.message['academic_year_start']){
							frm.set_value("academic_year_start",r.message['academic_year_start'])
						}
						if (r.message['academic_year_end']){
							frm.set_value("academic_year_end",r.message['academic_year_end'])
						}
					}
				} 
			}); 
		}
	}
});
