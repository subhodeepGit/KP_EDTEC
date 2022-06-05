frappe.listview_settings['Student Attendance'] = {
	add_fields: [ "status"],
	get_indicator: function(doc) {
		if (doc.status=="Absent") {
			return [__("Absent"), "orange", "status,=,Absent"];
		}
		else if (doc.status=="Present") {
			return [__("Present"), "green", "status,=,Present"];
		}
		else if (doc.status=="On Leave") {
			return [__("On Leave"), "grey", "status,=,On Leave"];
		}
	}
};
