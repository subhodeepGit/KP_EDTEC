frappe.ui.form.on('Program', {
	setup: function(frm) {
		frm.set_query("course","courses", function() {
			return {
				filters: {
					"disable":0
				}
			};
		});
	}
});