frappe.ui.form.on('Department', {
	setup(frm) {
        frm.set_df_property('program_grade', 'reqd', 1);
        frm.set_query("department", function() {
			return {
				filters: {
					"is_group":0,
					"is_stream":0
				}
			};
		});
    }

});