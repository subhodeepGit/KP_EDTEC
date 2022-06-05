frappe.listview_settings['Placement Drive Application'] = {
	add_fields: ["status"],
	get_indicator: function(doc) {
        if (doc.docstatus==1 && doc.status=="Applied") {
			return [__(doc.status), "blue"];
		}
        else if (doc.docstatus==1 && doc.status=="Rejected") {
			return [__(doc.status), "red"];
		}
        else if (doc.docstatus==1 && doc.status=="Hired") {
			return [__(doc.status), "green"];
		}
	}
};