cur_frm.add_fetch('course','course_name','course_name');
cur_frm.add_fetch('course','course_code','course_code');
frappe.ui.form.on('Course Enrollment', {
    refresh(frm){
        cur_frm.dashboard.hide()
        frm.set_df_property('credit_distribution', 'cannot_add_rows', true);
        cur_frm.doc.credit_distribution.forEach(data=>{
            var df = frappe.meta.get_docfield("Credit distribution List", "assessment_criteria",data.name);
            df.read_only=1;
        })
        

    },
	// setup(frm) {
    //     frm.set_query("course", function() {
    //         return {
    //             query: 'kp_edtec.kp_edtec.doctype.course_enrollment.get_course',
    //             filters: {
    //                 "program_enrollment":frm.doc.program_enrollment
    //             }
    //         };
    //     });
	// },
    total_course_marks:function(frm){
		(frm.doc.credit_distribution).forEach(data=>{
			var d = locals[data.doctype][data.name];
			d.total_marks=(frm.doc.total_course_marks*(d.weightage/100))
			refresh_field("total_marks", d.name, d.parentfield);	
		})
	},
})

frappe.ui.form.on("Credit distribution List", "weightage", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.total_marks=(frm.doc.total_course_marks*(d.weightage/100))
	refresh_field("total_marks", d.name, d.parentfield);
});