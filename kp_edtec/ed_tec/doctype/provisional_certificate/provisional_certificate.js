// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Provisional Certificate', {
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) { 
					frm.set_value("date",frappe.datetime.get_today())
					
					if(r.message){
						if (r.message['prn']){
							frm.set_value("permanent_registration_number",r.message['prn'])
						}
						if (r.message['programs']){
							frm.set_value("programs",r.message['programs'])
						}
					}
				} 
			}); 
		}
	}
});
