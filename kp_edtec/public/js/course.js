frappe.ui.form.on('Course', {
	refresh: function(frm) {
        frm.remove_custom_button("Add to Programs","Action");
		frm.remove_custom_button("Add to Semester","Action");
		if (!cur_frm.doc.__islocal && (!frappe.user.has_role(["Student","Instructor"]) || frappe.user.has_role(["System Manager"]))) {
			frm.add_custom_button(__('Add to Semester'), function() {
				frm.trigger('add_course_to_semester')
			}, __('Action'));
		}
	},
	disable:function(frm){
        if(frm.doc.disable == 1){
        	frappe.call({
				method: "kp_edtec.ed_tec.doctype.course.check_for_semester",
				args:{
					"course":frm.doc.name
				},
				callback: function(r) {
					if(r.message){
						frappe.throw(__('Course <b>{0}</b> found in <b>{1}</b> to disable remove the course from semester.',[frm.doc.name, r.message]));
					}
				}
			});
        }
	},
	setup:function(frm){
		frm.remove_custom_button("Add to Programs","Action");
		frm.set_query("program", function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
	},
	total_marks:function(frm){
		(frm.doc.credit_distribution).forEach(data=>{
			var d = locals[data.doctype][data.name];
			d.total_marks=(frm.doc.total_marks*(d.weightage/100))
			refresh_field("total_marks", d.name, d.parentfield);	
		})
	},
	add_course_to_semester: function(frm) {
		get_semester_without_course(frm.doc.name).then(r => {
			if (r.message.length) {
				frappe.prompt([
					{
						fieldname: 'programs',
						label: __('Semester'),
						fieldtype: 'MultiSelectPills',
						get_data: function() {
							return r.message;
						}
					}
				],
				function(data) {
					frappe.call({
						method: 'kp_edtec.ed_tec.doctype.course.add_course_to_programs',
						args: {
							'course': frm.doc.name,
							'programs': data.programs,
						},
						callback: function(r) {
							if (!r.exc) {
								frm.reload_doc();
							}
						},
						freeze: true,
						freeze_message: __('...Adding Course to Semester')
					})
				}, __('Add Course to Semester'), __('Add'));
			} else {
				frappe.msgprint(__('This course is already added to the existing semester'));
			}
		});
	}
});


let get_semester_without_course = function(course) {
	return frappe.call({
		args:{"course":course},
		method: 'kp_edtec.ed_tec.doctype.course.get_semesters_name',
	});
}
// frappe.ui.form.on("Course Credit", "lectures", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
// 	d.total=((d.lectures||0)+(d.tutorials||0)+(d.practicals||0))
// 	refresh_field("total", d.name, d.parentfield);
// });
// frappe.ui.form.on("Course Credit", "tutorials", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
// 	d.total=((d.lectures||0)+(d.tutorials||0)+(d.practicals||0))
// 	refresh_field("total", d.name, d.parentfield);
// });
// frappe.ui.form.on("Course Credit", "practicals", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
// 	d.total=((d.lectures||0)+(d.tutorials||0)+(d.practicals||0))
// 	refresh_field("total", d.name, d.parentfield);
// });
// frappe.ui.form.on('Course Credit', {
// 	course_credit_add: function(frm, cdt, cdn){
// 		cur_frm.fields_dict['course_credit'].grid.wrapper.find('.grid-add-row').hide();
// 	}
// })
frappe.ui.form.on("Credit distribution List", "weightage", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.total_marks=(frm.doc.total_marks*(d.weightage/100))
	refresh_field("total_marks", d.name, d.parentfield);
});