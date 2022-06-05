// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Department Academic Calender', {
	setup(frm){
		frm.set_query("academic_calendar_template", function() {
			return {
				filters: {
					"programs":frm.doc.program,
					"academic_year":frm.doc.academic_year
				}
			};
		});
	},
	program:function(frm){
		if(frm.doc.program){
			frappe.db.get_value("Programs", {'name':frm.doc.program},'department', resp => {
				frm.set_value("department",resp.department)
			})
		}

	},
	academic_calendar_template(frm){
		if(frm.doc.academic_calendar_template){
			frappe.call({
				method: "kp_edtec.ed_tec.doctype.academic_calender.academic_calender.get_academic_events_table",
				args:{
					"academic_calendar_template":frm.doc.academic_calendar_template,
				},
				callback: function(r) {
					if(r.message) {
						frm.clear_table("academic_events_table");
						$.each(r.message || [], function(i, d) {
						var row=frm.add_child("academic_events_table")
						row.academic_events=d.academic_events
						row.start_date=d.start_date
						row.end_date=d.end_date
						row.duration=d.duration
						});
						frm.refresh_field("academic_events_table")
					}
				}
			})
		}
	}
});
