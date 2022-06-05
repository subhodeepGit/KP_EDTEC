// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Programs', {
	setup(frm) {
        frm.set_df_property('program_grade', 'reqd', 1);
		frm.set_df_property('program_grade', 'reqd', 1);
        frm.set_query("department", function() {
			return {
				filters: {
					"is_group":0,
					"is_stream":0
				}
			};
		});
		frm.set_query("semesters","semesters", function(_doc, cdt, cdn) {
            return {
                filters: {
                    "programs":frm.doc.name
                }
            };
        });
    },
	refresh(frm){
		if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role('System Manager')){
			frm.set_df_property('add_semesters', 'hidden', 1);
		}
	},
	add_semesters: function(frm) {
		if (!frm.doc.__unsaved){
			if (!frm.doc.programs_abbreviation){
				frappe.throw("Program Abbrevation Missing for Create Semesters")
			}
			frm.set_value("semesters",[]);
			frappe.call({
				method: "create_semesters",
				doc:frm.doc,
				callback: function(r) { 
				if (r.message['semesters']){
					frm.set_value("semesters",[]);
					(r.message['semesters']).forEach(element => {
						var row = frm.add_child("semesters")
						row.semesters=element
						row.semesters_name=element
						frm.refresh_field("semesters")
					});
					if(r.message['is_existing']){
						frm.save();
					}
					// frm.save();
					else{
						frm.reload_doc();
					}
					
					// window.location.reload();
				}
				} 
				
			});  
		}
		else{
			frappe.throw("Please Save Document First")
		}		
	},
	add_courses: function(frm) {
		let table_values = [];
		let dialog = new frappe.ui.Dialog({
			title: __("Add Courses"),
			width: 400,
			fields: [
				{
					fieldname: "course_table", fieldtype: "Table",
					in_place_edit: true, data: table_values,
					get_data: () => {
						return table_values;
					},
					fields: [
							{
							"fieldname": "course",
							"fieldtype": "Link",
							"in_list_view": 1,
							"label": "Course",
							"options": "Course",
							"reqd": 1
						   },
						   {
							"fieldname": "modes",
							"fieldtype": "Select",
							"in_list_view": 1,
							"label": "Modes",
							"options": "\nTheory\nPractical\nBoth",
						   },
						   {
							"default": "1",
							"fieldname": "required",
							"fieldtype": "Check",
							"in_list_view": 1,
							"label": "Mandatory"
						   }
					]
				},
			],
			primary_action: function() {
				dialog.hide();
				(dialog.get_values()['course_table']).forEach(element => {
					var c = frm.add_child("courses")
                	c.course=element.course
					c.course_name=element.course
					c.modes=element.modes
				})
				frm.refresh_field("courses")
			},
			primary_action_label: __('Add')
		});
		dialog.show();
			
	}
});
frappe.ui.form.on("Semesters", "add_courses", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	let table_values = [];
	let dialog = new frappe.ui.Dialog({
		title: __("Add Courses"),
		width: 400,
		fields: [
			{
				fieldname: "course_table", fieldtype: "Table",
				in_place_edit: true, data: table_values,
				get_data: () => {
					return table_values;
				},
				fields: [
						{
						"fieldname": "course",
						"fieldtype": "Data",
						"in_list_view": 1,
						"label": "Course",
						"reqd": 1
					   },
					   {
						"fieldname": "mode",
						"fieldtype": "Select",
						"in_list_view": 1,
						"label": "Mode",
						"options": "Theory\nPractical\nBoth",
						"default":"Theory"
					   },
				]
			},
		],
		primary_action: function() {
			dialog.hide();
			    frappe.call({
						method:"kp_edtec.ed_tec.doctype.programs.programs.create_courses",
						args: {
							program:frm.doc.name,
							semester:d.semesters,
							courses: dialog.get_values()['course_table']
						}
  				})
		},
		primary_action_label: __('Add')
	});
	dialog.show();

});
frappe.ui.form.on("Semesters", "go_to_course_list", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	frappe.set_route('List', 'Course', {program: d.semesters});
});