frappe.listview_settings['Photocopy Application'] = {
    get_indicator: function (doc) {
		if (doc.status=="Phocopy Uploaded") {
			return [__("Phocopy Uploaded"), "green", "status,=,Phocopy Uploaded"];
		} 
	}
};