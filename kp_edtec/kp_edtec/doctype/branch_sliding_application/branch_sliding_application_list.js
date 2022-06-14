frappe.listview_settings['Branch Sliding Application'] = {
	get_indicator: function(doc) {
        if(doc.status == "Approved") {
			return [__("Approved"), "green"];
		}
		else if(doc.status == "Applied")  {
			return [__("Applied"), "orange"];
		} 
		else if(doc.status == "Rejected") {
			return [__("Rejected"), "red"];
		}
	}
};