// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leaving Certificate', {
	student: function(frm) {
		if(frm.doc.student){
			frappe.call({
				doc:frm.doc,
				method: "get_missing_fields",
				callback: function(r) {
				    frm.set_value("date",frappe.datetime.get_today()) 
					if(r.message){
						if (r.message['prn']){
							frm.set_value("prn_number",r.message['prn'])
						}
						if (r.message['guardian']){
							frm.set_value("father_name",r.message['guardian'])
						}
						if (r.message['class']){
							frm.set_value("class_in_which_studying",r.message['class'])
						}
						if (r.message['address']){
							frm.set_value("permanent_address",r.message['address'])
						} 
						if (r.message['date_of_birth']){
							frm.set_value("date_of_birth",r.message['date_of_birth'])
						} 
						if (r.message['mothers_name']){
							frm.set_value("mothers_name",r.message['mothers_name'])
						} 
						if (r.message['father_name']){
							frm.set_value("father_name",r.message['father_name'])
						}
						if (r.message['village']){
							frm.set_value("village",r.message['village'])
						}
						if (r.message['police_station']){
							frm.set_value("police_station",r.message['police_station'])
						} 
						if (r.message['post_office']){
							frm.set_value("post_office",r.message['post_office'])
						} 
						if (r.message['district']){
							frm.set_value("district",r.message['district'])
						} 
						if (r.message['pincodex']){
							frm.set_value("pincodex",r.message['pincodex'])
						} 
						if (r.message['enrollment_dte']){
							frm.set_value("date_of_admission_as_in_the_admission_register",r.message['enrollment_dte'])
						} 
					}
				} 
			}); 
		}
	}
});
