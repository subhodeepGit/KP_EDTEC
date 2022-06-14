cur_frm.add_fetch('student_group','class_room','room');
frappe.ui.form.on('Course Scheduling Tool', {
	setup: function(frm) {
        frm.set_query("instructor", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.course_scheduling_tool.get_instructor',
				filters: {
					"course":frm.doc.course
				}
			};
		});
		frm.set_query("course", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.course_scheduling_tool.get_course',
				filters: {
					"program":frm.doc.program
				}
			};
		});
    },
	instructor:function(frm){
		frappe.confirm(
			'Do You Want To Add <b>Additional Instructors</b>?',
			function(){
				frm.trigger("additional_instructor")
			},
			function(){
				window.close();
			}
		)
	},
	additional_instructor:function(frm){
		var d = new frappe.ui.Dialog({
			title: __('Additional Instructors'),
			fields:[{fieldtype:'Table', fieldname: 'instructor_list',label:"Instructor List",
			fields: [
				{
					"label" : "Instructor",
					"fieldname": "instructor",
					"fieldtype": "Link",
					"options":"Instructor",
					"in_list_view":1,
					get_query: function () {
						return {
							query: 'kp_edtec.kp_edtec.doctype.course_schedule.get_instructor',
                			filters:{"course":frm.doc.course}
						}
					},
					onchange: function() {
						Object.values(d.get_value('instructor_list')).forEach(i=>{
							frappe.db.get_value('Instructor', {name: i.instructor}, ['instructor_name'], (r) => {
								i['instructor_name']=r.instructor_name
								d.fields_dict.instructor_list.grid.refresh();
							})
							})
							d.fields_dict.instructor_list.grid.refresh();
					}
				},
				{
					"label" : "Instructor Name",
					"fieldname": "instructor_name",
					"fieldtype": "Data",
					"in_list_view":1
				}
			]
			}],
			primary_action: function() {
				(frm.doc)["additional_instructors"]=d.get_values();
				d.hide();
			},
			primary_action_label: __('Add')
		});
		d.show();
	}
});