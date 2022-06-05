frappe.ui.form.on("Student Group", {
    refresh:function(frm){
        if (frm.doc.group_based_on=="Exam Declaration"){
            frm.remove_custom_button("Student Attendance Tool","Tools");
            frm.remove_custom_button("Course Scheduling Tool","Tools");
            frm.remove_custom_button("Newsletter","View");
            frm.remove_custom_button("Add Guardians to Email Group","Actions");
        }
		if (frm.doc.group_based_on =="Mentor-Mentee"){
            
            frm.remove_custom_button("Course Scheduling Tool","Tools");

        }
        if (!frm.doc.__islocal && frappe.user.has_role(["System Manager"]) && frm.doc.group_based_on !="Mentor-Mentee"){
            frm.remove_custom_button("Course Schedule","Create");
            frm.add_custom_button(__("Course Schedule"), function() {
                frappe.model.open_mapped_doc({
                    method: "kp_edtec.ed_tec.doctype.student_group.create_course_schedule",
                    frm: frm,
                });
            }, __('Create'))
        }
        
        
        if(cur_frm.doc.students){
			if((cur_frm.doc.students).length!=0){
				cur_frm.page.add_menu_item(__('Bulk Email'), function() { 
					frappe.call({
						method: 'kp_edtec.ed_tec.doctype.student_group.get_student_emails',
						args: {
							students: frm.doc.students
						},
						callback: function(resp){
							if(resp.message){
								new frappe.views.CommunicationComposer({
									doc: cur_frm.doc,
									frm: cur_frm,
									subject: __(cur_frm.meta.name) + ': ' + cur_frm.docname,
									recipients:resp.message, 
									attach_document_print: false,
							});
							}
						}
					})
				});
			}
		}
        frm.set_query('course', function(doc) {
	        if(frm.doc.group_based_on=='Exam Declaration' && frm.doc.exam_declaration){
                return {
                    query:"kp_edtec.ed_tec.doctype.student_group.get_courses_from_ed",
                    filters: {
                        "exam_declaration":frm.doc.exam_declaration
                    }
                };
            }else{
            	return {
					query: 'kp_edtec.ed_tec.doctype.student_group.filter_courses',
					filters:{"program":frm.doc.program}
				};
			}
        });
    },
	setup:function(frm){
		frm.set_query("exam_declaration", function() {
			return {
				filters:{
					"docstatus":1,
					"disabled":0
			    }
			};
		});
		frm.set_df_property("student_category","hidden",1)
		if(frm.doc.group_based_on == "Mentor-Mentee"){
			frm.set_df_property("academic_year","reqd",0)
			frm.set_df_property("academic_term","reqd",0)
			frm.set_df_property("student_category","reqd",0)
			frm.set_df_property("academic_year","hidden",1)
			frm.set_df_property("academic_term","hidden",1)
			
		}
		else{
			frm.set_df_property("academic_year","reqd",1)
			frm.set_df_property("academic_term","reqd",1)
			// frm.set_df_property("student_category","reqd",1)
			frm.set_df_property("academic_year","hidden",0)
			frm.set_df_property("academic_term","hidden",0)
			// frm.set_df_property("student_category","hidden",0)
		}
		frm.set_query("program", function() {
			if(frm.doc.group_based_on == "Exam Declaration" && frm.doc.exam_declaration){
				return {
					query: 'kp_edtec.ed_tec.doctype.student_group.get_semester_by_exam_declaration',
					filters: {
						"exam_declaration":frm.doc.exam_declaration
					}
				};
			}
			else{
				return {
					filters: {
						"programs":frm.doc.programs
					}
				};
			}
		});

		frm.fields_dict['multiples_programs'].grid.get_field('programs').get_query = function(doc, cdt, cdn) {
            return {   
                query: 'kp_edtec.ed_tec.doctype.student_group.filter_programs_by_course', 
                filters:{
                    "course":frm.doc.course
                }
            }
        }
		if(frm.doc.group_based_on=='Exam Declaration' && frm.doc.exam_declaration){
            frm.set_query('course', function(doc) {
                return {
                    query:"kp_edtec.ed_tec.doctype.student_group.get_courses_from_ed",
                    filters: {
                        "exam_declaration":frm.doc.exam_declaration
                    }
                };
            });
        }else{
        	frm.set_query("course", function() {
				return {
					query: 'kp_edtec.ed_tec.doctype.student_group.filter_courses',
					filters:{"program":frm.doc.program}
				};
			});
        }
        
	},
    get_student: function(frm) {
        frm.clear_table('students')
		if (frm.doc.group_based_on == 'Batch' || frm.doc.group_based_on == 'Course') {
			var student_list = [];
			var max_roll_no = 0;
			$.each(frm.doc.students, function(_i,d) {
				student_list.push(d.student);
				if (d.group_roll_number>max_roll_no) {
					max_roll_no = d.group_roll_number;
				}
			});

			if (frm.doc.academic_year) {
				frappe.call({
					method: 'kp_edtec.ed_tec.doctype.student_group.get_students',
					args: {
						'academic_year': frm.doc.academic_year,
						'academic_term': frm.doc.academic_term,
						'group_based_on': frm.doc.group_based_on,
						'program': frm.doc.program,
						'batch' : frm.doc.batch,
						'student_category' : frm.doc.student_category,
						'course': frm.doc.course
					},
					callback: function(r) {
						if (r.message) {
							$.each(r.message, function(i, d) {
								if(!in_list(student_list, d.student)) {
									var s = frm.add_child('students');
									s.student = d.student;
									s.student_name = d.student_name;
									if (d.active === 0) {
										s.active = 0;
									}
									s.group_roll_number = ++max_roll_no;
								}
							});
							refresh_field('students');
							frm.save();
						} else {
							frappe.msgprint(__('Student Group is already updated.'))
						}
					}
				})
			}
		}
		else if(frm.doc.group_based_on == "Combined Course"){
			console.log("z")
			frappe.call({
                method: 'kp_edtec.ed_tec.doctype.student_group.get_student_based_on_combined_course',
                args: {
					filters:{
						course: frm.doc.course,
						programs_list:frm.doc.multiples_programs,
						academic_year: frm.doc.academic_year,
                    	max_strength: frm.doc.max_strength
					}
                },
                callback: function(resp){
                    if(resp.message){
                        resp.message.map(std => {
                            let row = frm.add_child("students")
                            row.student = std.student
                            row.student_name = std.student_name
                        })
                        frm.refresh_field('students')
                    }
                }
            })
		}
        else if(frm.doc.group_based_on == "Exam Declaration"){
			if (!frm.doc.exam_declaration){
				frappe.msgprint("Please Select Exam Declaration First")
			}
			else{
				frappe.db.get_doc("Exam Declaration", frm.doc.exam_declaration).then(( declaration  ) => {
					frappe.call({
						method: "frappe.client.get_value",
						args: {
							doctype: "Exam Application",
							filters: {exam_declaration: frm.doc.exam_declaration, 'docstatus':1},
						    fieldname: 'name'
						},
						callback: function(r) {
							if(!r.message.name && declaration.is_application_required){
								frappe.msgprint("There are no exam application filled againsed this exam declaration",frm.doc.exam_declaration)
							}
						}
					});
				});
			}
			if (!frm.doc.programs){
				frappe.msgprint("Please Select Programs First")
			}


           if (frm.doc.exam_declaration && frm.doc.programs){
			frappe.call({
                method: 'kp_edtec.ed_tec.doctype.student_group.get_student_based_on_exam_declaration',
                args: {
					exam_declaration:frm.doc.exam_declaration,
					semester:frm.doc.program,
					course:frm.doc.course,
					academic_year:frm.doc.academic_year,
                    academic_term: frm.doc.academic_term,
                    max_strength: frm.doc.max_strength
                },
                callback: function(resp){
                    if(resp.message){
                        resp.message.map(std => {
                            let row = frm.add_child("students")
                            row.student = std.student
                            row.student_name = std.student_name
                        })
                        frm.refresh_field('students')
                    }
                }
            })
		   }


        } 
        else {
			frappe.msgprint(__('Select students manually for the Activity based Group'));
		}
	},
    before_save: function(frm){
        if(frm.doc.max_strength > frm.doc.total_capacity){
            frappe.throw(__("Max strength can not exceed total capacity"))
        }
    },
	group_based_on:function(frm){
        if (frm.doc.group_based_on != "Batch" || frm.doc.group_based_on != "Course"){
           frm.set_value('student_group_name',"");
			frm.set_value('class_room',"");
			frm.set_value('total_capacity',"");
			frm.set_value('max_strength',"");
			frm.set_value('programs',"");
			frm.set_value('program',"");
			frm.set_value('course',"");
        }
		frm.set_value('instructors',[]);
		if(frm.doc.group_based_on == "Batch"){
			frm.set_df_property("batch","reqd",1)
		}
		else{
			frm.set_df_property("batch","reqd",0)
		}
		frm.trigger("add_courses_in_child");
	},
	program:function(frm){
		frm.set_value('instructors',[]);
		frm.trigger("add_courses_in_child");
	},
	course:function(frm){
		frm.set_value('instructors',[]);
		if (frm.doc.group_based_on == "Exam Declaration" && frm.doc.exam_declaration){
			frm.set_value("exam_schedule_date",'')
			frm.set_value("from_time",'')
			frm.set_value("to_time",'')
			frappe.db.get_doc("Exam Declaration", frm.doc.exam_declaration).then(( declaration  ) => {
				(declaration.courses_offered).forEach((  course_row ) => {
					if (course_row.courses==frm.doc.course){
						frm.set_value("exam_schedule_date",course_row.examination_date)
						frm.set_value("from_time",course_row.from_time)
						frm.set_value("to_time",course_row.to_time)
					 }
				})
			});
		}
	},
	academic_year:function(frm){
		frm.set_value('instructors',[]);
	},
	exam_declaration:function(frm){
		frm.set_value('instructors',[]);
		frm.set_value("academic_year",'')
		frm.set_value("academic_term",'')
		frm.set_value("course",'')
		if (frm.doc.exam_declaration){
			frappe.db.get_doc("Exam Declaration", frm.doc.exam_declaration).then(( declaration  ) => {
				frm.set_value("academic_term",declaration.academic_term)
				frm.set_value("academic_year",declaration.academic_year)
			});
		}
	},
	generate_roll_no:function(frm){
		if (!frm.doc.roll_number_series){
			frappe.throw("Please Select Naming Series")
		}
		if (!frm.doc.students || (frm.doc.students).length==0){
			frappe.throw("Please select the students first in below student table")
		}
		if (frm.doc.roll_number_series){
			frappe.call({
				method: 'kp_edtec.ed_tec.doctype.student_group.generate_roll_no',
				args: {
					selected_naming:frm.doc.roll_number_series,
					name:frm.doc.name,
					students:frm.doc.students
				},
				callback: function(resp){
					frm.reload_doc();
				}
			})
		}
		else{
			frappe.throw("Select <b>Roll Number Series</b> First")
		}
	}
})
frappe.ui.form.on('Student Group Instructor', {
	instructors_add: function(frm, cdt, cdn){
		var course_options="\n"
		var instructor_options=''
		var semesters=[]
		if (frm.doc.group_based_on == 'Course' || frm.doc.group_based_on =="Combined Course"){
			course_options=frm.doc.course
			semesters.push(frm.doc.program)
		}
		else if (frm.doc.group_based_on == 'Batch' || frm.doc.group_based_on == 'Activity'){
			semesters.push(frm.doc.program)
			frappe.call({
				method: 'kp_edtec.ed_tec.doctype.student_group.get_courses',
				args: {
					semester: frm.doc.program
				},
				callback: function(resp){
					if(resp.message){
						course_options=resp.message
						d.set_df_property('course', 'options', course_options);
					}
				}
			})
		}
		else if (frm.doc.group_based_on == "Exam Declaration" && frm.doc.exam_declaration){
			semesters.push(frm.doc.program)
			frappe.call({
				method: 'kp_edtec.ed_tec.doctype.student_group.get_courses_on_declaration',
				args: {
					declaration: frm.doc.exam_declaration
				},
				callback: function(resp){
					if(resp.message){
						course_options=resp.message
						d.set_df_property('course', 'options', course_options);
					}
				}
			})
		}
		var d = new frappe.ui.Dialog({
			title: __('Add Instructor'),
			fields: [
				{
					"label" : "Course",
					"fieldname": "course",
					"fieldtype": "Select",
					"reqd":1,
					"options": course_options,
					onchange: function() {
						var course=d.get_value('course');
						d.set_value("instructor","");
						if (course){
							frappe.call({
								method: 'kp_edtec.ed_tec.doctype.student_group.get_instructor',
								args: {
									filters:
										{
											academic_year: frm.doc.academic_year,
											course:course,
											semesters:semesters,
											apply_semester_filter:frm.doc.group_based_on=="Combined Course"?0:1
										}
								},
								callback: function(resp){
									if(resp.message){
										instructor_options=resp.message
										d.set_df_property('instructor', 'options', instructor_options);
									}
								}
							})
						}
					}
				},
				{
					"label" : "Instructor",
					"fieldname": "instructor",
					"fieldtype": "Select",
					"reqd":1,
					"options": instructor_options
				}
			],
			primary_action: function() {
				var values = d.get_values();
				var row = frappe.get_doc(cdt, cdn);
				row.course=values.course
				row.instructor=values.instructor
				frappe.db.get_value("Course", {'name':values.course},['course_code','course_name'], resp => {
					row.course_code = resp.course_code
					row.course_name = resp.course_name
					frm.refresh_field('instructors')
				})
				frm.refresh_field('instructors')
				d.hide();
			},
			primary_action_label: __('Add Values')
		});
		d.show();
	}
});