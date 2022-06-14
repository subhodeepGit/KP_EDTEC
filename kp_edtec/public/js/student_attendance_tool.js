frappe.ui.form.on('Student Attendance Tool', {
    refresh:function(frm){
        frm.set_df_property('based_on', 'options', ['Student Group', 'Course Schedule', 'Hostel']);
        frm.set_df_property('date', 'depends_on','eval:(["Student Group","Hostel"].includes(doc.based_on))');
		// frm.set_df_property('attendance', 'depends_on','eval: (doc.course_schedule || (doc.student_group && doc.date) || (doc.building && doc.date))');
		frm.set_df_property('attendance', 'depends_on','eval: (doc.course_schedule || (doc.student_group && doc.date))');
    },
    based_on:function(frm){
		
        if (frm.doc.based_on=="Hostel" && frm.doc.date){
			frm.set_value("course_schedule", "");
			frm.set_value("student_group", "");
            frm.trigger("hostel_fields")
        }
    },
    hostel_fields:function(frm){
        var dialog = new frappe.ui.Dialog({
			title: __('Hostel Details'),
			fields: [
				{
					"label" : "Hostel Category",
					"fieldname": "hostel_category",
					"fieldtype": "Link",
					"options": "Hostel Category"
				},
                {
					"label" : "Building",
					"fieldname": "building",
					"fieldtype": "Link",
					"options": "Building",
					"reqd":1,
					get_query: function () {
						if (dialog.get_value("hostel_category")){
							return {
								filters:{"hostel_category":dialog.get_value("hostel_category")}
							}
						}
					}
				},
				{
					"label" : "Hostel Room",
					"fieldname": "hostel_room",
					"fieldtype": "Link",
					"options": "Hostel Room",
					get_query: function () {
						return {
							filters:{"building":dialog.get_value("building")}
						}
						
					}
				},
			],
			primary_action: function() {
				var data = dialog.get_values();
				frm.doc.hostel_category=dialog.get_value("hostel_category");
				frm.doc.building=dialog.get_value("building");
				frm.doc.hostel_room=dialog.get_value("hostel_room");
                if (data.building) {
					frm.trigger("building")
                    dialog.hide();
                }
			},
			primary_action_label: __('Get Students')
		});
		dialog.show();
    },
	building:function(frm){
		var method = "kp_edtec.kp_edtec.doctype.student_attendance_tool.get_student_records";
		frm.set_df_property('attendance', 'depends_on','eval: (doc.course_schedule || (doc.student_group && doc.date) || doc.date)');
		frappe.call({
			method: method,
			args: {
				building: frm.doc.building,
				hostel_room:frm.doc.hostel_room
			},
			callback: function(r) {
				if (!frm.students_area) {
					frm.students_area = $('<div>')
						.appendTo(frm.fields_dict.students_html.wrapper);
				}
				var students = r.message || [];
				frm.students_editor = new education.StudentsEditor(frm, frm.students_area, students);
			}
		})
	},
    date:function(frm){
        if (frm.doc.based_on=="Hostel" && frm.doc.date){
            frm.trigger("hostel_fields")
        }
    },
    
    student_group:function(frm){
        if (frm.doc.based_on=="Student Group" && !frm.doc.date){
            if (frm.doc.group_based_on == 'Batch' || frm.doc.group_based_on == 'Course'){
	            var dialog = new frappe.ui.Dialog({
					fields: [
		                {
							"label" : "Course Schedule",
							"fieldname": "course_schedule",
							"fieldtype": "Link",
							"options" : "Course Schedule",
							"reqd":1,
							get_query: function () {
							   if (frm.doc.student_group){
									return {
										filters:{"student_group":frm.doc.student_group}
									}
								}
						    }
						}
					],
					primary_action: function() {
						var data = dialog.get_values();
						frappe.db.get_value('Course Schedule', {'name':data.course_schedule},'schedule_date', resp => {
			        		frm.set_value('date', resp.schedule_date)
			        	});
		                dialog.hide(); 
					}
				});
				dialog.show();
			}
        }
    }
});


education.StudentsEditor = Class.extend({
	init: function(frm, wrapper, students) {
		this.wrapper = wrapper;
		this.frm = frm;
		if(students.length > 0) {
			this.make(frm, students);
		} else {
			this.show_empty_state();
		}
	},
	make: function(frm, students) {
		var me = this;

		$(this.wrapper).empty();
		var student_toolbar = $('<p>\
			<button class="btn btn-default btn-add btn-xs" style="margin-right: 5px;"></button>\
			<button class="btn btn-xs btn-default btn-remove" style="margin-right: 5px;"></button>\
			<button class="btn btn-default btn-primary btn-mark-att btn-xs"></button></p>').appendTo($(this.wrapper));

		student_toolbar.find(".btn-add")
			.html(__('Check all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if (!$(check).prop("disabled")) {
						check.checked = true;
					}
				});
			});

		student_toolbar.find(".btn-remove")
			.html(__('Uncheck all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if (!$(check).prop("disabled")) {
						check.checked = false;
					}
				});
			});

		student_toolbar.find(".btn-mark-att")
			.html(__('Mark Attendance'))
			.on("click", function() {
				$(me.wrapper.find(".btn-mark-att")).attr("disabled", true);
				var studs = [];
				$(me.wrapper.find('input[type="checkbox"]')).each(function(i, check) {
					var $check = $(check);
					studs.push({
						student: $check.data().student,
						student_name: $check.data().studentName,
						group_roll_number: $check.data().group_roll_number,
						disabled: $check.prop("disabled"),
						checked: $check.is(":checked")
					});
				});

				var students_present = studs.filter(function(stud) {
					return !stud.disabled && stud.checked;
				});

				var students_absent = studs.filter(function(stud) {
					return !stud.disabled && !stud.checked;
				});

				frappe.confirm(__("Do you want to update attendance? <br> Present: {0} <br> Absent: {1}",
					[students_present.length, students_absent.length]),
					function() {	//ifyes
						if(!frappe.request.ajax_count) {
							frappe.call({
								method: "erpnext.education.api.mark_attendance",
								freeze: true,
								freeze_message: __("Marking attendance"),
								args: {
									"students_present": students_present,
									"students_absent": students_absent,
									"student_group": frm.doc.student_group,
									"course_schedule": frm.doc.course_schedule,
									"building": frm.doc.building,
									"hostel_category": frm.doc.hostel_category,
									"attendance_for":frm.doc.based_on=="Hostel"?"Hosteler":"",
									"date": frm.doc.date
								},
								callback: function(r) {
									$(me.wrapper.find(".btn-mark-att")).attr("disabled", false);
									frm.trigger("student_group");
								}
							});
						}
					},
					function() {	//ifno
						$(me.wrapper.find(".btn-mark-att")).attr("disabled", false);
					}
				);
			});

		var htmls = students.map(function(student) {
			return frappe.render_template("student_button_custom", {
				student: student.student,
				student_name: student.student_name,
				group_roll_number: student.group_roll_number,
				status: student.status
			})
		});

		$(htmls.join("")).appendTo(me.wrapper);
	},

	show_empty_state: function() {
		$(this.wrapper).html(
			`<div class="text-center text-muted" style="line-height: 100px;">
				${__("No Students in")} ${this.frm.doc.student_group}
			</div>`
		);
	}
});