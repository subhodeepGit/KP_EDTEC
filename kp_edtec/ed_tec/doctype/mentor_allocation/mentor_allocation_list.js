frappe.listview_settings['Mentor Allocation'] = {
	onload: function(listview) {
		if (!frappe.route_options & frappe.user.has_role(["Student"]) && !frappe.user.has_role(["System Manager"])){ 
			$(".filter-selector").hide();
            frappe.route_options = {
                "user": ["=", frappe.session.user],
				"docstatus":1
            };
		}
	}
};