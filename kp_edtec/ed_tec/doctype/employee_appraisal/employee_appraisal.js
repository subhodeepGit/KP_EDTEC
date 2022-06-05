// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt
var total_score = 0.0
frappe.ui.form.on('Employee Appraisal', {
	kra_template: function(frm) {
		if(frm.doc.kra_template){
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Employee Appraisal Template",
					filters: {name: frm.doc.kra_template}
				},
				callback: function(r) {
					if(r.message){
						if(!r.message.teaching_activity){
							frm.set_df_property('teaching_activity', 'hidden', 1);
						}
						if(!r.message.seminars_and_guest_lecture){
							frm.set_df_property('seminars_and_guest_lecture', 'hidden', 1);
						}
						if(!r.message.examination_duties){
							frm.set_df_property('examination_duties', 'hidden', 1);
						}
						if(!r.message.additional_resources){
							frm.set_df_property('additional_resources', 'hidden', 1);
						}
						if(!r.message.innovative_teaching_learning){
							frm.set_df_property('innovative_teaching_learning', 'hidden', 1);
						}
						if(!r.message.co_curricular_extension_professional_development){
							frm.set_df_property('co_curricular_extension_professional_development', 'hidden', 1);
						}
						if(!r.message.published_paper){
							frm.set_df_property('published_paper', 'hidden', 1);
						}
						if(!r.message.article_and_chapters_published){
							frm.set_df_property('article_and_chapters_published', 'hidden', 1);
						}
						if(!r.message.conference__proceedings){
							frm.set_df_property('conference__proceedings', 'hidden', 1);
						}
						if(!r.message.book_published){
							frm.set_df_property('book_published', 'hidden', 1);
						}
						if(!r.message.research_project_and_counsltancies){
							frm.set_df_property('research_project_and_counsltancies', 'hidden', 1);
						}
						if(!r.message.research_guidance){
							frm.set_df_property('research_guidance', 'hidden', 1);
						}
						if(!r.message.instructor_development_program){
							frm.set_df_property('instructor_development_program', 'hidden', 1);
						}
						if(!r.message.paper_presented){
							frm.set_df_property('paper_presented', 'hidden', 1);
						}
						if(!r.message.invited_lecture_and_chairmanship){
							frm.set_df_property('invited_lecture_and_chairmanship', 'hidden', 1);
						}
						if(!r.message.patent){
							frm.set_df_property('patent', 'hidden', 1);
						}
						if(!r.message.policy_document){
							frm.set_df_property('policy_document', 'hidden', 1);
						}
						if(!r.message.awards_and_fellowship){
							frm.set_df_property('awards_and_fellowship', 'hidden', 1);
						}
						if(!r.message.translation_work){
							frm.set_df_property('translation_work', 'hidden', 1);
						}
						if(!r.message.design_of_new_curriculum_and_course){
							frm.set_df_property('design_of_new_curriculum_and_course', 'hidden', 1);
						}
						if(!r.message.moocs){
							frm.set_df_property('moocs', 'hidden', 1);
						}
						if(!r.message.e_content){
							frm.set_df_property('e_content', 'hidden', 1);
						}
						if(!r.message.book_published){
							frm.set_df_property('book_published', 'hidden', 1);
						}
						if(!r.message.administrative_activity){
							frm.set_df_property('administrative_activity', 'hidden', 1);
						}
						if(!r.message.ict_mediated_teaching_learning_pedagogy_and_content){
							frm.set_df_property('ict_mediated_teaching_learning_pedagogy_and_content', 'hidden', 1);
						}
					}
				}
			});
		}
	},
	validate:function(frm){
		if (!cur_frm.doc.__islocal && cur_frm.doc.administrative_activity){
            if((cur_frm.doc.administrative_activity).length == 0){
	            var d = frm.add_child("administrative_activity");
	            d.score = 'Not-satisfactory';
	            frm.refresh_field("administrative_activity");
		   }
		
			else if (((cur_frm.doc.administrative_activity).length-1) == 1 || ((cur_frm.doc.administrative_activity).length-1) == 2){
	        $.each(frm.doc.administrative_activity, function(index, row){
	            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
		            row.score = 'Satisfactory';
		            frm.set_df_property( row.score, 'read-only', 1)
		            frm.refresh_field("administrative_activity");
	            }
	            else if(row.score=='' && row.name_of_job != ''){
	            	var d = frm.add_child("administrative_activity");
	            	d.score = 'Satisfactory';
	            	frm.set_df_property( row.score, 'read-only', 1)
		            frm.refresh_field("administrative_activity");
	            }
	        });
			}
			else if (((frm.doc.administrative_activity).length-1) >= 3){
		        $.each(frm.doc.administrative_activity, function(index, row){
		            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
		            	row.score = "Good";
			            frm.refresh_field("administrative_activity");
		            }
		            else if(row.score==''){
			            var d = frm.add_child("administrative_activity");
			            d.score = "Good";
			            frm.refresh_field("administrative_activity");
		            }
		        });
			}
		}
		if (!cur_frm.doc.__islocal && frm.doc.examination_duties ){
            if(frm.doc.examination_duties.length == 0){
	            var d = frm.add_child("examination_duties");
	            d.score = 'Not-satisfactory';
	            frm.refresh_field("examination_duties");
	        }
		
			else if ((frm.doc.examination_duties.length-1) == 1 || (frm.doc.examination_duties.length-1) == 2){
		        $.each(frm.doc.examination_duties, function(index, row){
		            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
			            row.score = 'Satisfactory';
			            frm.set_df_property( row.score, 'read-only', 1)
			            frm.refresh_field("examination_duties");
		            }
		            else if(row.score=='' && row.name_of_job != ''){
		            	var d = frm.add_child("examination_duties");
		            	d.score = 'Satisfactory';
		            	frm.set_df_property( row.score, 'read-only', 1)
			            frm.refresh_field("examination_duties");
		            }
		        });
			}
			else if ((frm.doc.examination_duties.length-1) >= 3 ){
		        $.each(frm.doc.examination_duties, function(index, row){
		            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
		            	row.score = "Good";
			            frm.refresh_field("examination_duties");
		            }
		            else if(row.score==''){
			            var d = frm.add_child("examination_duties");
			            d.score = "Good";
			            frm.refresh_field("examination_duties");
		            }
		        });
			}
		}
		if (!cur_frm.doc.__islocal && frm.doc.co_curricular_extension_professional_development){
           if(frm.doc.co_curricular_extension_professional_development.length == 0){
            var d = frm.add_child("co_curricular_extension_professional_development");
            d.score = 'Not-satisfactory';
            frm.refresh_field("co_curricular_extension_professional_development");
			}
		
			else if ((frm.doc.co_curricular_extension_professional_development.length-1) == 1 || (frm.doc.co_curricular_extension_professional_development.length-1) == 2){
		        $.each(frm.doc.co_curricular_extension_professional_development, function(index, row){
		            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
			            row.score = 'Satisfactory';
			            frm.set_df_property( row.score, 'read-only', 1)
			            frm.refresh_field("co_curricular_extension_professional_development");
		            }
		            else if(row.score=='' && row.name_of_job != ''){
		            	var d = frm.add_child("co_curricular_extension_professional_development");
		            	d.score = 'Satisfactory';
		            	frm.set_df_property( row.score, 'read-only', 1)
			            frm.refresh_field("co_curricular_extension_professional_development");
		            }
		        });
			}
			else if ((frm.doc.co_curricular_extension_professional_development.length-1) >= 3 ){
		        $.each(frm.doc.co_curricular_extension_professional_development, function(index, row){
		            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
		            	row.score = "Good";
			            frm.refresh_field("co_curricular_extension_professional_development");
		            }
		            else if(row.score==''){
			            var d = frm.add_child("co_curricular_extension_professional_development");
			            d.score = "Good";
			            frm.refresh_field("co_curricular_extension_professional_development");
		            }
		        });
			}
		}
	},
	refresh:function(frm){
		if (!cur_frm.doc.__islocal){
			$.each(frm.doc.administrative_activity, function(index, row){
	            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
		            cur_frm.fields_dict['administrative_activity'].grid.wrapper.find('.grid-add-row').hide();
	            }
	        });
	        $.each(frm.doc.co_curricular_extension_professional_development, function(index, row){
	            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
		            cur_frm.fields_dict['co_curricular_extension_professional_development'].grid.wrapper.find('.grid-add-row').hide();
	            }
	        });
	        $.each(frm.doc.examination_duties, function(index, row){
	            if (row.score == "Good" || 'Satisfactory' || 'Not-satisfactory'){
		            cur_frm.fields_dict['examination_duties'].grid.wrapper.find('.grid-add-row').hide();
	            }
	        });
		}
	},
	employee: function(frm) {
		if(frm.doc.employee){
			frappe.model.with_doc("Employee", frm.doc.employee, function() {
	            var tabletransfer= frappe.model.get_doc("Employee", frm.doc.employee)
	            if(tabletransfer.education){
	            	frm.clear_table("employee_education");
		            $.each(tabletransfer.education, function(index, row){
		                var d = frm.add_child("employee_education");
		                d.school_univ = row.school_univ;
		                d.qualification = row.qualification ;
		                d.level = row.level;
		                d.year_of_passing = row.year_of_passing;
		                d.class_per = row.class_per;
		                d.maj_opt_subj = row.maj_opt_subj;
		                frm.refresh_field("employee_education");
		            });
	            }
	            if (tabletransfer.internal_work_history){
	            	frm.clear_table("employee_current_work");
		            $.each(tabletransfer.internal_work_history, function(index, row){
		                var d = frm.add_child("employee_current_work");
		                	d.branch = row.branch;
		                	d.department = row.department ;
		                	d.designation = row.designation;
		                	d.from_date = row.from_date;
		                	d.to_date = row.to_date;
		                frm.refresh_field("employee_current_work");
		            });
		        }   
	            if(tabletransfer.external_work_history){
	            	frm.clear_table("employee_previous_work_history");
		            $.each(tabletransfer.external_work_history, function(index, row){
		                var d = frm.add_child("employee_previous_work_history");
		                d.company_name = row.company_name;
		                d.salary = row.salary ;
		                d.designation = row.designation;
		                d.address = row.address;
		                d.contact = row.contact;
		                d.total_experience = row.total_experience;
		                frm.refresh_field("employee_previous_work_history");
		            });
		        }
	        });
	        if(frm.doc.academic_year){
				frappe.call({
					method: "kp_edtec.ed_tec.doctype.employee_appraisal.employee_appraisal.get_academic_courses",
					args: {
						employee: frm.doc.employee,
						academic_year: frm.doc.academic_year
					},
					callback: function(r) {
						if(r.message){
							frm.clear_table("teaching_activity");
							$.each(r.message || [], function(i, d) {
								var row=frm.add_child("teaching_activity")
								row.course = d.course
								row.course_name = d.course_name
								row.course_code = d.course_code
								row.hours_per_week_alloted = d.hrs
								row.classes_attended = d.class_attended
								row._classes_taken = d.classes_taken
								row.score = d.score
							});
							cur_frm.refresh_fields("teaching_activity");

							frm.clear_table("additional_resources");
							$.each(r.message || [], function(i, d) {
								var row=frm.add_child("additional_resources")
								row.course=d.course
							});
							cur_frm.refresh_fields("additional_resources");
						}
					}
				});
			}
			else{
	           frappe.msgprint("Please fill the academic year.")
			}
		}
	}
})
frappe.ui.form.on('Invited Lecture And Chairmanship', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International (Abroad)" ){
	    	if(d.score > 7){
	    		frappe.msgprint(__("Score of International (Abroad) Level in row no {0} in <b>Invited Lecture And Chairmanship</b> must be less than or equal to <b>7</b>",[d.idx]));
				d.score = 0;
				refresh_field('score', d.name, 'invited_lecture_and_chairmanship');
	    	}
		}
		else if (d.level == "International (within country)" ){
	    	if(d.score > 5){
	    		frappe.msgprint(__("Score of International (within country) Level in row no {0} in <b>Invited Lecture And Chairmanship</b> must be less than or equal to <b>5</b>",[d.idx]));
				d.score = 0;
				refresh_field('score', d.name, 'invited_lecture_and_chairmanship');
	    	}
		}
		else if (d.level == "National" && d.score > 3){
	    	frappe.msgprint(__("Score of National Level in row no {0} in <b>Invited Lecture And Chairmanship</b> must be less than or equal to <b>3</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'invited_lecture_and_chairmanship');
		}
		else if (d.level == "University" && d.score > 2){
	    	frappe.msgprint(__("Score of University Level in row no {0} in <b>Invited Lecture And Chairmanship</b> must be less than or equal to <b>2</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'invited_lecture_and_chairmanship');
		}
	},
	level: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International (Abroad)" ){
	    	d.research_score_claimed = 7;
	    	if(d.score > 7){
				d.score = 7;
	    	}
	    	refresh_field('research_score_claimed', d.name, 'invited_lecture_and_chairmanship');
		}
		else if (d.level == "International (within country)" ){
	    	d.research_score_claimed = 5;
	    	if(d.score > 5){
				d.score = 5;
	    	}
	    	refresh_field('research_score_claimed', d.name, 'invited_lecture_and_chairmanship');
		}
		else if (d.level == "National"){
	    	d.research_score_claimed = 3;
	    	if(d.score > 3){
                d.score = 3;
	    	}
			refresh_field('research_score_claimed', d.name, 'invited_lecture_and_chairmanship');
		}
		else if (d.level == "University"){
			d.research_score_claimed = 2;
			if (d.score > 2){
                d.score = 2;
            }
			refresh_field('research_score_claimed', d.name, 'invited_lecture_and_chairmanship');
		}
	},
	research_score_claimed: function(frm, cdt, cdn) {
		frm.trigger('level')
	}
});
frappe.ui.form.on('Published Paper', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.no_of_co_author == 2){
            if(d.score > (12 * 70)/100){
            	frappe.msgprint(__("Score of row no {0} in <b>Published Paper</b> must be less than or equal to <b>{1}</b>",[d.idx, (12 * 70)/100] ));
				d.score = 0;
				refresh_field('score', d.name, 'published_paper');
            }
		}
		else if (d.no_of_co_author > 2){
				if(d.main_author == 1){
	                if(d.score > (12 * 70)/100){
	                	frappe.msgprint(__("Score of row no {0} in <b>Published Paper</b> must be less than or equal to <b>{1}</b>",[d.idx,(12 * 70)/100] ));
						d.score = 0;
						refresh_field('score', d.name, 'published_paper');
	                }
	            }
	            else{
	                if(d.score > (12 * 30)/100){
	                	frappe.msgprint(__("Score of row no {0} in <b>Published Paper</b> must be less than or equal to <b>{1}</b>",[d.idx,(12 * 30)/100] ));
						d.score = 0;
						refresh_field('score', d.name, 'published_paper');
	                }
	            }
        }    
	},
	wos_url_link:function(frm, cdt, cdn){
	    var d = locals[cdt][cdn];
	   if(d.wos_url_link =='Journal Papers indexed in UGC – CARE list') {
          d.research_score_claimed = 15
          refresh_field('research_score_claimed', d.name, 'published_paper');
	   }
	},
	thomson_reuters_impact_factor:function(frm, cdt, cdn){
		var d = locals[cdt][cdn];
		if(d.thomson_reuters_impact_factor < 1){
			d.research_score_claimed = 6
			refresh_field('research_score_claimed', d.name, 'published_paper');
	   	    if(d.score > 6){
	   	    	d.score = 6
	   	    	frappe.msgprint(__("Score of row no {0} in <b>Published Paper</b> must be less than or equal to <b>{1}</b>",[d.idx,6] ));
	   	    	refresh_field('score', d.name, 'published_paper');
	   	    }
		}
		else if(d.thomson_reuters_impact_factor < 2 && d.thomson_reuters_impact_factor > 1){
	   	    d.research_score_claimed = 11
	   	    refresh_field('research_score_claimed', d.name, 'published_paper');
	   	    if(d.score > 11){
	   	    	d.score = 11
	   	        frappe.msgprint(__("Score of row no {0} in <b>Published Paper</b> must be less than or equal to <b>{1}</b>",[d.idx,11] ));
	   	    	refresh_field('score', d.name, 'published_paper');
	   	    }
	    }
	    else if(d.thomson_reuters_impact_factor < 5 && d.thomson_reuters_impact_factor > 2){
	   	    d.research_score_claimed = 16
	   	    refresh_field('research_score_claimed', d.name, 'published_paper');
	   	    if(d.score > 16){
	   	    	d.score = 16
	   	        frappe.msgprint(__("Score of row no {0} in <b>Published Paper</b> must be less than or equal to <b>{1}</b>",[d.idx,16] ));
	   	    	refresh_field('score', d.name, 'published_paper');
	   	    }
	    }
	    else if(d.thomson_reuters_impact_factor < 10 && d.thomson_reuters_impact_factor > 5){
	   	    d.research_score_claimed = 21
	   	    refresh_field('research_score_claimed', d.name, 'published_paper');
	   	    if(d.score > 21){
	   	    	d.score = 21
	   	        frappe.msgprint(__("Score of row no {0} in <b>Published Paper</b> must be less than or equal to <b>{1}</b>",[d.idx,21] ));
	   	    	refresh_field('score', d.name, 'published_paper');
	   	    }
	    }
	    else if(d.thomson_reuters_impact_factor > 10){
	   	    d.research_score_claimed = 26
	   	    refresh_field('research_score_claimed', d.name, 'published_paper');
	   	    if(d.score > 26){
	   	    	d.score = 26
	   	        frappe.msgprint(__("Score of row no {0} in <b>Published Paper</b> must be less than or equal to <b>{1}</b>",[d.idx,26] ));
	   	    	refresh_field('score', d.name, 'published_paper');
	   	    }
	    }
	},
	research_score_claimed:function(frm, cdt, cdn){
		frm.trigger('thomson_reuters_impact_factor')
	}
});
frappe.ui.form.on('Book Published', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.level == "International"){
			if(!d.no_of_co_authors){
			    if(d.publication_type == "Book"){
		            if(d.author_type == "Main author"){
		            	 if(d.score > 12 ){
		                	frappe.msgprint(__("Score of single author for book in International level in  row no {0} in <b>Book Published</b> must be less than or equal to <b>12</b>",[d.idx ]));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
		            else if(d.author_type == 'Editor'){
						if(d.score > 10 ){
		                	frappe.msgprint(__("Score of single Editor for book in International level in  row no {0} in <b>Book Published</b> must be less than or equal to <b>10</b>",[d.idx ]));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
					}
		        }
	            else if(d.publication_type == "Chapter"){
	            	 if(d.score > 5 ){
	                	frappe.msgprint(__("Score of single author for chapter in International level in  row no {0} in <b>Book Published</b> must be less than or equal to <b>5</b>",[d.idx ]));
						d.score = 0;
						refresh_field('score', d.name, 'book_published');
	                }
	            }
			}
			else if (d.no_of_co_authors > 0){
				if(d.publication_type == "Book"){
		            if( d.author_type == "Main author"){
		                if(d.score > (12 * 70)/100){
		                	frappe.msgprint(__("Score of main author for book in International level row no {0} in <b>Book Published</b> must be less than or equal to <b>{1}</b>",[d.idx, (12 * 70)/100] ));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
		            else if(d.author_type == "Co-author"){
		            	if(d.score > (12 * 30)/100){
		                	frappe.msgprint(__("Score of co-author for book in International level row no {0} in <b>Book Published</b> must be less than or equal to <b>{1}</b>",[d.idx, (12 * 30)/100] ));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
		            else if(d.author_type == 'Editor'){
						if(d.score > 10 ){
		                	frappe.msgprint(__("Score of Editor for book in joint publication in International level in  row no {0} in <b>Book Published</b> must be less than or equal to <b>10</b>",[d.idx ]));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
					}
		        }
		        else if(d.publication_type == "Chapter"){
		        	if(d.author_type == "Main author"){
		                if(d.score > (5 * 70)/100){
		                	frappe.msgprint(__("Score of main author for chapter in International level row no {0} in <b>Book Published</b> must be less than or equal to <b>{1}</b>",[d.idx, (5 * 70)/100] ));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
		            else if(d.author_type == "Co-author"){
		            	if(d.score > (5 * 30)/100){
		                	frappe.msgprint(__("Score of co-author for chapter in International level row no {0} in <b>Book Published</b> must be less than or equal to <b>{1}</b>",[d.idx, (5 * 30)/100] ));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
		        }
			}
		}
		else if(d.level == "National"){
			if(d.publication_type == "Book"){
				if(!d.no_of_co_authors){
		            if(d.author_type == "Main author"){
		            	 if(d.score > 10 ){
		                	frappe.msgprint(__("Score of single author for book in National level row no {0} in <b>Book Published</b> must be less than or equal to <b>10</b>",[d.idx ]));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
				}
				else if (d.no_of_co_authors > 0){
		            if(d.author_type == "Main author"){
		                if(d.score > (10 * 70)/100){
		                	frappe.msgprint(__("Score of main author for book in National level row no {0} in <b>Book Published</b> must be less than or equal to <b>{1}</b>",[d.idx, (10 * 70)/100] ));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
		            else if(d.author_type == "Co-author") {
		            	if(d.score > (10 * 30)/100){
		                	frappe.msgprint(__("Score of co-author for book in National level row no {0} in <b>Book Published</b> must be less than or equal to <b>{1}</b>",[d.idx, (10 * 30)/100] ));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
		            else if(d.author_type == 'Editor'){
						if(d.score > 8 ){
		                	frappe.msgprint(__("Score of Editor for book in National level in  row no {0} in <b>Book Published</b> must be less than or equal to <b>8</b>",[d.idx ]));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
					}
				}
			}
			if(d.publication_type == "Chapter"){
				if(!d.no_of_co_authors){
		            if(d.author_type == "Main author"){
		            	 if(d.score > 5 ){
		                	frappe.msgprint(__("Score of single author for chapter in National level row no {0} in <b>Book Published</b> must be less than or equal to <b>5</b>",[d.idx ]));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
				}
				else if (d.no_of_co_authors > 0){
		            if(d.author_type == "Main author"){
		                if(d.score > (5 * 70)/100){
		                	frappe.msgprint(__("Score of main author for chapter in National level row no {0} in <b>Book Published</b> must be less than or equal to <b>{1}</b>",[d.idx, (5 * 70)/100] ));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
		            else if(d.author_type == "Co-author") {
		            	if(d.score > (5 * 30)/100){
		                	frappe.msgprint(__("Score of co-author for chapter in National level row no {0} in <b>Book Published</b> must be less than or equal to <b>{1}</b>",[d.idx, (5 * 30)/100] ));
							d.score = 0;
							refresh_field('score', d.name, 'book_published');
		                }
		            }
				}
			}
		}
	},
	author_type: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.level == "International"){
			if(!d.no_of_co_authors){
			    if(d.publication_type == "Book"){
		            if(d.author_type == "Main author"){
		            	d.research_score_claimed = 12 
		            	if(d.score > 12 ){
							d.score = 12;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
		            else if(d.author_type == 'Editor'){
						d.research_score_claimed = 10
						if(d.score > 10 ){
							d.score = 10;
		                }
		                refresh_field('score', d.name, 'book_published');
					}
		        }
	            else if(d.publication_type == "Chapter"){
	            	d.research_score_claimed = 5;
	            	if(d.score > 5 ){
						d.score = 5;
	                }
	                refresh_field('score', d.name, 'book_published');
	            }
			}
			else if (d.no_of_co_authors > 0){
				if(d.publication_type == "Book"){
		            if( d.author_type == "Main author"){
		                d.research_score_claimed = (12 * 70)/100
		                if(d.score > (12 * 70)/100){
							d.score = (12 * 70)/100;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
		            else if(d.author_type == "Co-author"){
		            	d.research_score_claimed =(12 * 30)/100;
		            	if(d.score > (12 * 30)/100){
							d.score =(12 * 30)/100;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
		            else if(d.author_type == 'Editor'){
						d.research_score_claimed = 10;
						if(d.score > 10 ){
							d.score = 10;
		                }
		                refresh_field('score', d.name, 'book_published');
					}
		        }
		        else if(d.publication_type == "Chapter"){
		        	if( d.author_type == "Main author"){
		                d.research_score_claimed = (5 * 70)/100;
		                if(d.score > (5 * 70)/100){
							d.score = (5 * 70)/100;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
		            else if(d.author_type == "Co-author"){
		            	d.research_score_claimed = (5 * 30)/100;
		            	if(d.score > (5 * 30)/100){
							d.score = (5 * 30)/100;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
		        }
			}
		}
		else if(d.level == "National"){
			if(d.publication_type == "Book"){
				if(!d.no_of_co_authors){
		            if( d.author_type == "Main author"){
		            	d.research_score_claimed = 10;
		            	if(d.score > 10 ){
							d.score = 10;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
				}
				else if (d.no_of_co_authors > 0){
		            if( d.author_type == "Main author"){
		                d.research_score_claimed = (10 * 70)/100;
		                if(d.score > (10 * 70)/100){
							d.score = (10 * 70)/100;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
		            else if(d.author_type == "Co-author") {
		            	d.research_score_claimed = (10 * 30)/100;
		            	if(d.score > (10 * 30)/100){
							d.score = (10 * 30)/100;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
		            else if(d.author_type == 'Editor'){
						d.research_score_claimed = 8;
						if(d.score > 8 ){
							d.score = 8;
		                }
		                refresh_field('score', d.name, 'book_published');
					}
				}
			}
			if(d.publication_type == "Chapter"){
				if(!d.no_of_co_authors){
		            if(d.author_type == "Main author"){
		            	d.research_score_claimed = 5;
		            	if(d.score > 5 ){
							d.score = 5;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
				}
				else if (d.no_of_co_authors > 0){
		            if(d.author_type == "Main author"){
		                d.research_score_claimed = (5 * 70)/100;
		                if(d.score > (5 * 70)/100){
							d.score = (5 * 70)/100;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
		            else if(d.author_type == "Co-author") {
		            	d.research_score_claimed = (5 * 30)/100;
		            	if(d.score > (5 * 30)/100){
							d.score = (5 * 30)/100;
		                }
		                refresh_field('score', d.name, 'book_published');
		            }
				}
			}
		}
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.level == "International"){
			if(!d.no_of_co_authors){
			    if(d.publication_type == "Book"){
		            if(d.author_type == "Main author"){
		            	if(d.research_score_claimed > 12 ){
							d.research_score_claimed = 12;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
		            else if(d.author_type == 'Editor'){
						if(d.research_score_claimed > 10 ){
							d.research_score_claimed = 10;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
					}
		        }
	            else if(d.publication_type == "Chapter"){
	            	if(d.research_score_claimed > 5 ){
						d.research_score_claimed = 5;
	                }
	                refresh_field('research_score_claimed', d.name, 'book_published');
	            }
			}
			else if (d.no_of_co_authors > 0){
				if(d.publication_type == "Book"){
		            if(d.author_type == "Main author"){
		                if(d.research_score_claimed > (12 * 70)/100){
							d.research_score_claimed = (12 * 70)/100;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
		            else if(d.author_type == "Co-author"){
		            	if(d.research_score_claimed > (12 * 30)/100){
							d.research_score_claimed =(12 * 30)/100;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
		            else if(d.author_type == 'Editor'){
						if(d.research_score_claimed > 10 ){
							d.research_score_claimed = 10;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
					}
		        }
		        else if(d.publication_type == "Chapter"){
		        	if(d.author_type == "Main author"){
		                if(d.research_score_claimed > (5 * 70)/100){
							d.research_score_claimed = (5 * 70)/100;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
		            else if( d.author_type == "Co-author"){
		            	if(d.research_score_claimed > (5 * 30)/100){
							d.research_score_claimed = (5 * 30)/100;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
		        }
			}
		}
		else if(d.level == "National"){
			if(d.publication_type == "Book"){
				if(!d.no_of_co_authors){
		            if(d.author_type == "Main author"){
		            	if(d.research_score_claimed > 10 ){
							d.research_score_claimed = 10;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
				}
				else if (d.no_of_co_authors > 0){
		            if(d.author_type == "Main author"){
		                if(d.research_score_claimed > (10 * 70)/100){
							d.research_score_claimed = (10 * 70)/100;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
		            else if(d.author_type == "Co-author") {
		            	if(d.research_score_claimed > (10 * 30)/100){
							d.research_score_claimed = (10 * 30)/100;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
		            else if(d.author_type == 'Editor'){
						if(d.research_score_claimed > 8 ){
							d.research_score_claimed = 8;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
					}
				}
			}
			if(d.publication_type == "Chapter"){
				if(!d.no_of_co_authors){
		            if(d.author_type == "Main author"){
		            	if(d.research_score_claimed > 5 ){
							d.research_score_claimed = 5;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
				}
				else if (d.no_of_co_authors > 0){
		            if(d.author_type == "Main author"){
		                if(d.research_score_claimed > (5 * 70)/100){
							d.research_score_claimed = (5 * 70)/100;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
		            else if(d.author_type == "Co-author") {
		            	if(d.research_score_claimed > (5 * 30)/100){
							d.research_score_claimed = (5 * 30)/100;
		                }
		                refresh_field('research_score_claimed', d.name, 'book_published');
		            }
				}
			}
		}
	}
});
frappe.ui.form.on('Paper Presented', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International (Abroad)" ){
	    	if(d.score >= 7){
	    		frappe.msgprint(__("Score of International (Abroad) Level in row no {0} in <b>Invited Lecture And Chairmanship</b> must be less than or equal to <b>7</b>",[d.idx]));
				d.score = 6;
				refresh_field('score', d.name, 'invited_lecture_and_chairmanship');
	    	}
		}
		else if (d.level == "International (within country)" ){
	    	if(d.score >= 5){
	    		frappe.msgprint(__("Score of International (within country) Level in row no {0} in <b>Invited Lecture And Chairmanship</b> must be less than or equal to <b>5</b>",[d.idx]));
				d.score = 4;
				refresh_field('score', d.name, 'invited_lecture_and_chairmanship');
	    	}
		}
		else if (d.level == "National" && d.score >= 3){
	    	frappe.msgprint(__("Score of National Level in row no {0} in <b>Invited Lecture And Chairmanship</b> must be less than or equal to <b>3</b>",[d.idx]));
			d.score = 2;
			refresh_field('score', d.name, 'invited_lecture_and_chairmanship');
		}
		else if (d.level == "University" && d.score >= 2){
	    	frappe.msgprint(__("Score of University Level in row no {0} in <b>Invited Lecture And Chairmanship</b> must be less than or equal to <b>2</b>",[d.idx]));
			d.score = 1;
			refresh_field('score', d.name, 'invited_lecture_and_chairmanship');
		}
	}
});
frappe.ui.form.on('Administrative Activity', {
	to: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.to && d.from) {
			var a = moment(d.to);
			var b = moment(d.from);
			d.duration = a.diff(b, 'days');
			refresh_field('duration', d.name, 'administrative_activity');
		}
	},
	from: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.to && d.from) {
			var a = moment(d.to);
			var b = moment(d.from);
			d.duration = a.diff(b, 'days');
			refresh_field('duration', d.name, 'administrative_activity');
		}
	}
});
frappe.ui.form.on('Co_Curricular Extension Professional Development', {
	to_time: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.to_time && d.from_time) {
			var a = moment(d.to_time);
			var b = moment(d.from_time);
			d.duration = a.diff(b, 'days');
			refresh_field('duration', d.name, 'co_curricular_extension_professional_development');
		}
	},
	from_time: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.to_time && d.from_time) {
			var a = moment(d.to_time);
			var b = moment(d.from_time);
			d.duration = a.diff(b, 'days');
			refresh_field('duration', d.name, 'co_curricular_extension_professional_development');
		}
	}
});
frappe.ui.form.on('Awards and Fellowship', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.level == "International" && d.score > 7){
        	frappe.msgprint(__("Final Score of row no {0} in <b>Awards and Fellowship</b> must be less than or equal to <b>7</b>",[d.idx]));
			d.score = 7;
			refresh_field('score', d.name, 'awards_and_fellowship');
		}
		else if (d.level == "National" && d.score > 5){
        	frappe.msgprint(__("Final Score of row no {0} in <b>Awards and Fellowship</b> must be less than or equal to <b>5</b> .",[d.idx] ));
			d.score = 5;
			refresh_field('score', d.name, 'awards_and_fellowship');
        }    
	},
	level: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.level == "International"){
			d.research_score_claimed = 7;
			refresh_field('research_score_claimed', d.name, 'awards_and_fellowship');
			if(d.score > 7){
				d.score = 7;
			}
			refresh_field('score', d.name, 'awards_and_fellowship');
		}
		else if (d.level == "National"){
			d.research_score_claimed = 5;
			refresh_field('research_score_claimed', d.name, 'awards_and_fellowship');
			if(d.score > 5){
                d.score = 5;
			}
			refresh_field('score', d.name, 'awards_and_fellowship');
        }    
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.level == "International"){
			if(d.research_score_claimed > 7){
				d.research_score_claimed = 7;
				refresh_field('research_score_claimed', d.name, 'awards_and_fellowship');
		    }
		}
		else if (d.level == "National"){
			d.research_score_claimed = 5;
			if(d.research_score_claimed > 5){
                d.research_score_claimed = 5;
				refresh_field('research_score_claimed', d.name, 'awards_and_fellowship');
		    }
		}
	}
});
frappe.ui.form.on('ICT MEDIATED TEACHING LEARNING PEDAGOGY AND CONTENT', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.score > 5){
        	frappe.msgprint(__("Final Score of row no {0} in <b>ICT MEDIATED TEACHING LEARNING PEDAGOGY AND CONTENT</b> must be less than or equal to <b>5</b>",[d.idx]));
			d.score = 5;
			refresh_field('score', d.name, 'ict_mediated_teaching_learning_pedagogy_and_content');
		}
	},
	level: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		d.research_score_claimed = 5
        refresh_field('research_score_claimed', d.name, 'ict_mediated_teaching_learning_pedagogy_and_content');
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.research_score_claimed > 5){
			d.research_score_claimed = 5
	        refresh_field('research_score_claimed', d.name, 'ict_mediated_teaching_learning_pedagogy_and_content');
		}
	}

});
frappe.ui.form.on('Translation Work', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.translation_category == "Chapter" || d.translation_category == "Research Paper"){
        	if (d.score > 3){
	        	frappe.msgprint(__("Final Score of Chapter or Research Paper in row no {0} in <b>Translation Work</b> must be less than or equal to <b>3</b>",[d.idx]));
				d.score = 3;
				refresh_field('score', d.name, 'translation_work');
			}
		}
		else if (d.translation_category == "Book"){
        	if (d.score > 8){
	        	frappe.msgprint(__("Final Score of Book in row no {0} in <b>Translation Work</b> must be less than or equal to <b>8</b> .",[d.idx] ));
				d.score = 8;
				refresh_field('score', d.name, 'translation_work');
	        }
        }    
	},
	translation_category: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.translation_category == "Chapter" || d.translation_category == "Research Paper"){
        	d.research_score_claimed = 3;
        	if (d.research_score_claimed > 3){
				d.research_score_claimed = 3;
			}
			refresh_field('research_score_claimed', d.name, 'translation_work');
		}
		else if (d.translation_category == "Book"){
			d.research_score_claimed = 8;
        	if (d.research_score_claimed > 8){
				d.research_score_claimed = 8;
	        }
	        refresh_field('research_score_claimed', d.name, 'translation_work');
        }
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.translation_category == "Chapter" || d.translation_category == "Research Paper"){
        	if (d.research_score_claimed > 3){
				d.research_score_claimed = 3;
				refresh_field('research_score_claimed', d.name, 'translation_work');
			}
		}
		else if (d.translation_category == "Book"){
        	if (d.research_score_claimed > 8){
				d.research_score_claimed = 8;
				refresh_field('research_score_claimed', d.name, 'translation_work');
	        }
        }
	}

});
frappe.ui.form.on('Design of New Curriculum and Course', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.score > 2){
	    	frappe.msgprint(__("Final Score in row no {0} in <b>Design of New Curriculum and Course</b> must be less than or equal to <b>2</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'design_of_new_curriculum_and_course');
		}
	},
	research_claimed_score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.research_claimed_score > 2){
			d.research_claimed_score = 2;
			refresh_field('research_claimed_score', d.name, 'design_of_new_curriculum_and_course');
		}
	},
	level: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		d.research_claimed_score = 2;
		refresh_field('research_claimed_score', d.name, 'design_of_new_curriculum_and_course');
	}
});
frappe.ui.form.on('Research Guidance', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.single__joint_supervisor == "Single Supervisor"){
			if(d.title == "Ph.D" && d.score > 10){
        	frappe.msgprint(__("Score of Ph.D for Single Supervisor in row no {0} in <b>Research Guidance</b> must be less than or equal to <b>10</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'research_guidance');
			}
			else if (d.title == "M.Phil" || d.title == "PG Dissertation"){
	        	if(d.score > 2){
                    frappe.msgprint(__("Score of M.Phil or PG Dissertation for Single Supervisor in row no {0} in <b>Research Guidance</b> must be less than or equal to <b>2</b> .",[d.idx] ));
					d.score = 0;
					refresh_field('score', d.name, 'research_guidance');
                }
	        } 
		}
		else if(d.single__joint_supervisor == "Joint Supervisor"){
			if(d.title == "Ph.D" && d.score > (10 * 70)/100){
	        	frappe.msgprint(__("Score of Ph.D for Joint Supervisor in row no {0} in <b>Research Guidance</b> must be less than or equal to <b>{1}</b>",[d.idx, (10 * 70)/100]));
				d.score = 0;
				refresh_field('score', d.name, 'research_guidance');
			}
			else if (d.title == "M.Phil" || d.title == "PG Dissertation"){
	        	if(d.score > (2 * 70)/100){
		        	frappe.msgprint(__("Score of M.Phil or PG Dissertation for Joint Supervisor in row no {0} in <b>Research Guidance</b> must be less than or equal to <b>{1}</b> .",[d.idx, (2 * 70)/100] ));
					d.score = 0;
					refresh_field('score', d.name, 'research_guidance');
	            }
	        } 
		}
		   
	},
	single__joint_supervisor: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.single__joint_supervisor == "Single Supervisor"){
			if(d.title == "Ph.D"){
				d.research_score_claimed = 10;
				if(d.research_score_claimed > 10){
                    d.research_score_claimed = 10;
				}
				refresh_field('research_score_claimed', d.name, 'research_guidance');
			}
			else if (d.title == "M.Phil" || d.title == "PG Dissertation"){
	        	d.research_score_claimed = 2;
	        	if(d.research_score_claimed > 2){
					d.research_score_claimed = 2;
                }
                refresh_field('research_score_claimed', d.name, 'research_guidance');
	        } 
		}
		else if(d.single__joint_supervisor == "Joint Supervisor"){
			if(d.title == "Ph.D"){
				d.research_score_claimed = (10 * 70)/100;
				if(d.research_score_claimed > (10 * 70)/100){
                    d.research_score_claimed = (10 * 70)/100;
				}
				refresh_field('research_score_claimed', d.name, 'research_guidance');
			}
			
			else if (d.title == "M.Phil" || d.title == "PG Dissertation"){
	        	d.research_score_claimed = (2 * 70)/100;
	        	if(d.research_score_claimed > (2 * 70)/100){
					d.research_score_claimed = (2 * 70)/100;
	            }
	            refresh_field('research_score_claimed', d.name, 'research_guidance');
	        } 
		}
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.single__joint_supervisor == "Single Supervisor"){
			if(d.title == "Ph.D"){
				if(d.research_score_claimed > 10){
                    d.research_score_claimed = 10;
				}
				refresh_field('research_score_claimed', d.name, 'research_guidance');
			}
			else if (d.title == "M.Phil" || d.title == "PG Dissertation"){
	        	if(d.research_score_claimed > 2){
					d.research_score_claimed = 2;
                }
                refresh_field('research_score_claimed', d.name, 'research_guidance');
	        } 
		}
		else if(d.single__joint_supervisor == "Joint Supervisor"){
			if(d.title == "Ph.D"){
				if(d.research_score_claimed > (10 * 70)/100){
                    d.research_score_claimed = (10 * 70)/100;
				}
				refresh_field('research_score_claimed', d.name, 'research_guidance');
			}
			
			else if (d.title == "M.Phil" || d.title == "PG Dissertation"){
	        	if(d.research_score_claimed > (2 * 70)/100){
					d.research_score_claimed = (2 * 70)/100;
	            }
	            refresh_field('research_score_claimed', d.name, 'research_guidance');
	        } 
		}
	}
});
frappe.ui.form.on('Research Project And Consultancies', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(!d.patent){
			if(d.status == "Completed Project"){
				if(d.grant_amount >= 1000000 && d.score > 5){
					frappe.msgprint(__("Score of Completed Project for Individual in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>5</b>",[d.idx]));
					d.score = 0;
					refresh_field('score', d.name, 'research_project_and_consultancies');
				}
				if(d.grant_amount < 1000000 && d.score > 2){
					frappe.msgprint(__("Score of Completed Project for Individual in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>2</b>",[d.idx]));
					d.score = 0;
					refresh_field('score', d.name, 'research_project_and_consultancies');
				}
			}
			else if (d.status == "Ongoing Project"){
				if(d.grant_amount >= 1000000 && d.score > 5){
		        	frappe.msgprint(__("Score of Ongoing Project for Individual in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>5</b> .",[d.idx] ));
					d.score = 0;
					refresh_field('score', d.name, 'research_project_and_consultancies');
		        }
		        if(d.grant_amount < 1000000 && d.score > 2){
		        	frappe.msgprint(__("Score of Ongoing Project for Individual in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>2</b> .",[d.idx] ));
					d.score = 0;
					refresh_field('score', d.name, 'research_project_and_consultancies');
		        }
	        } 
	        else if (d.status == "Consultancy Project"  && d.score > 3){
	        	frappe.msgprint(__("Score of Consultancy Project for Individual in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>3</b> .",[d.idx] ));
				d.score = 0;
				refresh_field('score', d.name, 'research_project_and_consultancies');
	        }
		}
		else if(d.patent){
			if(d.status == "Completed Project"){
				if(d.grant_amount > 1000000 && d.score > (5*50)/100){
					frappe.msgprint(__("Score of Completed Project for Joint in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>{1}</b>",[d.idx, (5*50)/100]));
					d.score = 0;
					refresh_field('score', d.name, 'research_project_and_consultancies');
				}
				if(d.grant_amount < 1000000 && d.score > (2*50)/100){
					frappe.msgprint(__("Score of Completed Project for Joint in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>{1}</b>",[d.idx, (2*50)/100]));
					d.score = 0;
					refresh_field('score', d.name, 'research_project_and_consultancies');
				}
			}
			else if (d.status == "Ongoing Project"){
				if(d.grant_amount > 1000000 && d.score > (5*50)/100){
		        	frappe.msgprint(__("Score of Ongoing Project for Joint in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>{1}</b> .",[d.idx, (5*50)/100] ));
					d.score = 0;
					refresh_field('score', d.name, 'research_project_and_consultancies');
		        }
		        if(d.grant_amount < 1000000 && d.score > (2*50)/100){
		        	frappe.msgprint(__("Score of Ongoing Project for Joint in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>{1}</b> .",[d.idx, (2*50)/100] ));
					d.score = 0;
					refresh_field('score', d.name, 'research_project_and_consultancies');
		        }
	        } 
	        else if (d.status == "Consultancy Project" && d.score > (3*50)/100){
	        	frappe.msgprint(__("Score of Consultancy Project for Joint in row no {0} in <b>Research Project And Consultancies</b> must be less than or equal to <b>{1}</b> .",[d.idx, (3*50)/100] ));
				d.score = 0;
				refresh_field('score', d.name, 'research_project_and_consultancies');
	        }
		}
	},
	grant_amount: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(!d.patent){
			if(d.status == "Completed Project"){
				if(d.grant_amount >= 1000000){
					d.research_score_claimed = 5;
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
					if(d.score > 5){
						d.score = 5;
					}
					refresh_field('score', d.name, 'research_project_and_consultancies');
				}
				if(d.grant_amount < 1000000){
					d.research_score_claimed = 2;
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
					if(d.score > 2){
						d.score = 2;
					}
					refresh_field('score', d.name, 'research_project_and_consultancies');
				}
			}
			else if (d.status == "Ongoing Project"){
				if(d.grant_amount >= 1000000){
					d.research_score_claimed = 5;
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
					if(d.score > 5){
                        d.score = 5;
					}
					refresh_field('score', d.name, 'research_project_and_consultancies');
		        }
		        if(d.grant_amount < 1000000){
					d.research_score_claimed = 2;
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
					if(d.score > 2){
						d.score = 2;
					}
					refresh_field('score', d.name, 'research_project_and_consultancies');
		        }
	        } 
	        else if (d.status == "Consultancy Project"){
				d.research_score_claimed = 3;
				refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
				if(d.score > 3){
					d.score = 3;
				}
				refresh_field('score', d.name, 'research_project_and_consultancies');
	        }
		}
		else if(d.patent){
			if(d.status == "Completed Project"){
				if(d.grant_amount > 1000000){
					d.research_score_claimed = (5*50)/100;
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
					if(d.score > (5*50)/100){
						d.score = (5*50)/100;
					}
					refresh_field('score', d.name, 'research_project_and_consultancies');
				}
				if(d.grant_amount < 1000000 ){
					d.research_score_claimed = (2*50)/100;
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
					if(d.score > (2*50)/100){
						d.score = (2*50)/100;
					}
					refresh_field('score', d.name, 'research_project_and_consultancies');
				}
			}
			else if (d.status == "Ongoing Project"){
				if(d.grant_amount > 1000000){
					d.research_score_claimed = (5*50)/100;
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
					if(d.score > (5*50)/100){
						d.score = (5*50)/100
					}
					refresh_field('score', d.name, 'research_project_and_consultancies');
		        }
		        if(d.grant_amount < 1000000){
					d.research_score_claimed = (2*50)/100;
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
					if(d.score > (2*50)/100){
						d.score = (2*50)/100
					}
					refresh_field('score', d.name, 'research_project_and_consultancies');
		        }
	        } 
	        else if (d.status == "Consultancy Project"){
				d.research_score_claimed = (3*50)/100;
				refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
				if(d.score > (3*50)/100){
                    d.score = (3*50)/100;
				}
				refresh_field('score', d.name, 'research_project_and_consultancies');
	        }
		}
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(!d.patent){
			if(d.status == "Completed Project"){
				if(d.grant_amount >= 1000000){
					d.research_score_claimed = 5;
					if(d.research_score_claimed > 5){
						d.research_score_claimed = 5;
					}
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
				}
				if(d.grant_amount < 1000000){
					d.research_score_claimed = 2;
					if(d.research_score_claimed > 2){
						d.research_score_claimed = 2;
					}
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
				}
			}
			else if (d.status == "Ongoing Project"){
				if(d.grant_amount >= 1000000){
					d.research_score_claimed = 5;
					if(d.research_score_claimed > 5){
                        d.research_score_claimed = 5;
					}
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
		        }
		        if(d.grant_amount < 1000000){
		        	d.research_score_claimed = 2;
					if(d.research_score_claimed > 2){
						d.research_score_claimed = 2;
					}
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
		        }
	        } 
	        else if (d.status == "Consultancy Project"){
	        	d.research_score_claimed = 3;
				if(d.research_score_claimed > 3){
					d.research_score_claimed = 3;
				}
				refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
	        }
		}
		else if(d.patent){
			if(d.status == "Completed Project"){
				if(d.grant_amount > 1000000){
					d.research_score_claimed = (5*50)/100;
					if(d.research_score_claimed > (5*50)/100){
						d.research_score_claimed = (5*50)/100;
					}
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
				}
				if(d.grant_amount < 1000000 ){
					d.research_score_claimed = (2*50)/100;
					if(d.research_score_claimed > (2*50)/100){
						d.research_score_claimed = (2*50)/100;
					}
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
				}
			}
			else if (d.status == "Ongoing Project"){
				if(d.grant_amount > 1000000){
					d.research_score_claimed = (5*50)/100
					if(d.research_score_claimed > (5*50)/100){
						d.research_score_claimed = (5*50)/100
					}
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
		        }
		        if(d.grant_amount < 1000000){
		        	d.research_score_claimed = (2*50)/100
					if(d.research_score_claimed > (2*50)/100){
						d.research_score_claimed = (2*50)/100
					}
					refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
		        }
	        } 
	        else if (d.status == "Consultancy Project"){
	        	d.research_score_claimed = (3*50)/100;
				if(d.research_score_claimed > (3*50)/100){
                    d.research_score_claimed = (3*50)/100;
				}
				refresh_field('research_score_claimed', d.name, 'research_project_and_consultancies');
	        }
		}
	}
});
frappe.ui.form.on('Patent', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International" ){
	    	if(d.score > 10){
	    		frappe.msgprint(__("Final Score of International Level in row no {0} in <b>Patent</b> must be less than or equal to <b>10</b>",[d.idx]));
				d.score = 0;
				refresh_field('score', d.name, 'patent');
	    	}
		}
		else if (d.level == "National" && d.score > 7){
	    	frappe.msgprint(__("Final Score of National Level in row no {0} in <b>Patent</b> must be less than or equal to <b>7</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'patent');
		}
	},
	level: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International" ){
			d.research_score_claimed = 10;
	    	refresh_field('research_score_claimed', d.name, 'patent');
	    	if(d.score > 10){
				d.score = 10;
	    	}
	    	refresh_field('score', d.name, 'patent');
		}
		else if (d.level == "National"){
			d.research_score_claimed = 7;
			refresh_field('research_score_claimed', d.name, 'patent');
			if(d.score > 7){
				d.score = 7;
			}
			refresh_field('score', d.name, 'patent');
		}
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International" ){
	    	if(d.research_score_claimed > 10){
				d.research_score_claimed = 10;
				refresh_field('research_score_claimed', d.name, 'patent');
	    	}
		}
		else if (d.level == "National"){
			if(d.research_score_claimed > 7){
				d.research_score_claimed = 7;
				refresh_field('research_score_claimed', d.name, 'patent');
			}
		}
	}
});
frappe.ui.form.on('Policy Document', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International" ){
	    	if(d.score > 10){
	    		frappe.msgprint(__("Final Score of International Level in row no {0} in <b>Policy Document</b> must be less than or equal to <b>10</b>",[d.idx]));
				d.score = 0;
				refresh_field('score', d.name, 'policy_document');
	    	}
		}
		else if (d.level == "National" && d.score > 7){
	    	frappe.msgprint(__("Final Score of National Level in row no {0} in <b>Policy Document</b> must be less than or equal to <b>7</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'policy_document');
		}
		else if (d.level == "State" && d.score > 4){
	    	frappe.msgprint(__("Final Score of State Level in row no {0} in <b>Policy Document</b> must be less than or equal to <b>4</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'policy_document');
		}
	},
	level: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International" ){
			d.research_score_claimed = 10;
			refresh_field('research_score_claimed', d.name, 'policy_document');
	    	if(d.final_score > 10){
				d.final_score = 10;
	    	}
	    	refresh_field('final_score', d.name, 'policy_document');
		}
		else if (d.level == "National" ){
			d.research_score_claimed = 7;
			refresh_field('research_score_claimed', d.name, 'policy_document');
			if(d.final_score > 7){
				d.final_score = 7;
			}
			refresh_field('final_score', d.name, 'policy_document');
		}
		else if (d.level == "State"){
			d.research_score_claimed = 4;
			refresh_field('research_score_claimed', d.name, 'policy_document');
			if(d.final_score > 4)
				d.final_score = 4;
			}
			refresh_field('final_score', d.name, 'policy_document');
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.level == "International" ){
	    	if(d.research_score_claimed > 10){
				d.research_score_claimed = 10;
				refresh_field('research_score_claimed', d.name, 'policy_document');
	    	}
		}
		else if (d.level == "National" ){
			if(d.research_score_claimed > 7){
				d.research_score_claimed = 7;
				refresh_field('research_score_claimed', d.name, 'policy_document');
			}
			
		}
		else if (d.level == "State"){
			if(d.research_score_claimed > 4)
			d.research_score_claimed = 4;
			refresh_field('research_score_claimed', d.name, 'policy_document');
		}
	}
});
frappe.ui.form.on('MOOCs', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.description == "Development of complete MOOCs in 4 quadrants" ){
	    	if(d.score > 20){
	    		frappe.msgprint(__("Final Score of Development of complete MOOCs in 4 quadrants in row no {0} in <b>MOOCs</b> must be less than or equal to <b>20</b>",[d.idx]));
				d.score = 0;
				refresh_field('score', d.name, 'moocs');
	    	}
		}
		else if (d.description == "MOOCs (developed in 4 quadrant) per Module/Lecture" && d.score > 5){
	    	frappe.msgprint(__("Final Score of MOOCs (developed in 4 quadrant) per Module/Lecture in row no {0} in <b>MOOCs</b> must be less than or equal to <b>5</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'moocs');
		}
		else if (d.description == "Content writer / Subject matter expert for each module of MOOCs" && d.score > 2){
	    	frappe.msgprint(__("Final Score of Content writer / Subject matter expert for each module of MOOCs in row no {0} in <b>MOOCs</b> must be less than or equal to <b>2</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'moocs');
		}
		else if (d.description == "Course co-ordiantor for MOOCs" && d.score > 8){
	    	frappe.msgprint(__("Final Score of Course co-ordiantor for MOOCs in row no {0} in <b>MOOCs</b> must be less than or equal to <b>8</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'moocs');
		}
	},
	description: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.description == "Development of complete MOOCs in 4 quadrants" ){
	    	d.research_score_claimed = 20;
	    	refresh_field('research_score_claimed', d.name, 'moocs');
	    	if(d.score > 20){
				d.score = 20;
	    	}
	    	refresh_field('score', d.name, 'moocs');
		}
		else if (d.description == "MOOCs (developed in 4 quadrant) per Module/Lecture"){
			d.research_score_claimed = 5;
			refresh_field('research_score_claimed', d.name, 'moocs');
			if(d.score > 5){
                d.score = 5;
			}
			refresh_field('score', d.name, 'moocs');
		}
		else if (d.description == "Content writer / Subject matter expert for each module of MOOCs"){
			d.research_score_claimed = 2;
			refresh_field('research_score_claimed', d.name, 'moocs');
			if(d.score > 2){
				d.score = 2;
			}
			refresh_field('score', d.name, 'moocs');
		}
		else if (d.description == "Course co-ordiantor for MOOCs"){
			d.research_score_claimed = 8;
			refresh_field('research_score_claimed', d.name, 'moocs');
			if(d.score > 8){
				d.score = 8;
			}
			refresh_field('score', d.name, 'moocs');
		}
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.description == "Development of complete MOOCs in 4 quadrants" ){
	    	if(d.research_score_claimed > 20){
				d.research_score_claimed = 20;
				refresh_field('research_score_claimed', d.name, 'moocs');
	    	}
		}
		else if (d.description == "MOOCs (developed in 4 quadrant) per Module/Lecture"){
			if(d.research_score_claimed > 5){
                d.research_score_claimed = 5;
                refresh_field('research_score_claimed', d.name, 'moocs');
			}
		}
		else if (d.description == "Content writer / Subject matter expert for each module of MOOCs"){
			if(d.research_score_claimed > 2){
				d.research_score_claimed = 2;
				refresh_field('research_score_claimed', d.name, 'moocs');
			}
		}
		else if (d.description == "Course co-ordiantor for MOOCs"){
			if(d.research_score_claimed > 8){
				d.research_score_claimed = 8;
				refresh_field('research_score_claimed', d.name, 'moocs');
			}
		}
	}
});
frappe.ui.form.on('E_Content', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.description == "Development of e-content in 4 quadrants for a course/e-Book" ){
	    	if(d.score > 12){
	    		frappe.msgprint(__("Final Score of Development e-content in 4 quadrants for a course/e-Book in row no {0} in <b>E_Content</b> must be less than or equal to <b>12</b>",[d.idx]));
				d.score = 0;
				refresh_field('score', d.name, 'e_content');
	    	}
		}
		else if (d.description == "Development of e-Content Module wise" && d.score > 5){
	    	frappe.msgprint(__("Final Score of Development of e-Content Module wise in row no {0} in <b>E_Content</b> must be less than or equal to <b>5</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'e_content');
		}
		else if (d.description == "Contribution of e-content module in course/paper/e-Book" && d.score > 2){
	    	frappe.msgprint(__("Final Score of Contribution of e-content module in course/paper/e-Book in row no {0} in <b>E_Content</b> must be less than or equal to <b>2</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'e_content');
		}
		else if (d.description == "Editor in e-content for complete course/paper/e-Book" && d.score > 10){
	    	frappe.msgprint(__("Final Score of Editor in e-content for complete course/paper/e-Book in row no {0} in <b>E_Content</b> must be less than or equal to <b>10</b>",[d.idx]));
			d.score = 0;
			refresh_field('score', d.name, 'e_content');
		}
	},
	description: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.description == "Development of e-content in 4 quadrants for a course/e-Book" ){
	    	d.research_score_claimed = 12;
	    	refresh_field('research_score_claimed', d.name, 'e_content');
	    	if(d.score > 12){
				d.score = 12;
	    	}
	    	refresh_field('score', d.name, 'e_content');
		}
		else if (d.description == "Development of e-Content Module wise"){
			d.research_score_claimed = 5;
			refresh_field('research_score_claimed', d.name, 'e_content');
			if(d.score > 5){
                d.score = 5;
			}
			refresh_field('score', d.name, 'e_content');
		}
		else if (d.description == "Contribution of e-content module in course/paper/e-Book"){
			d.research_score_claimed = 2;
			refresh_field('research_score_claimed', d.name, 'e_content');
			if(d.score > 2){
                d.score = 2;
			}
			refresh_field('score', d.name, 'e_content');
		}
		else if (d.description == "Editor in e-content for complete course/paper/e-Book"){
			d.research_score_claimed = 10;
			refresh_field('research_score_claimed', d.name, 'e_content');
			if(d.score > 10){
				d.score = 10;
			}
			refresh_field('score', d.name, 'e_content');
		}
	},
	research_score_claimed: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.description == "Development of e-content in 4 quadrants for a course/e-Book" ){
	    	if(d.research_score_claimed > 12){
				d.research_score_claimed = 12;
				refresh_field('research_score_claimed', d.name, 'e_content');
	    	}
		}
		else if (d.description == "Development of e-Content Module wise"){
			if(d.research_score_claimed > 5){
                d.research_score_claimed = 5;
                refresh_field('research_score_claimed', d.name, 'e_content');
			}
		}
		else if (d.description == "Contribution of e-content module in course/paper/e-Book"){
			if(d.research_score_claimed > 2){
                d.research_score_claimed = 2;
                refresh_field('research_score_claimed', d.name, 'e_content');
			}
		}
		else if (d.description == "Editor in e-content for complete course/paper/e-Book"){
			if(d.research_score_claimed > 10){
				d.research_score_claimed = 10;
				refresh_field('research_score_claimed', d.name, 'e_content');
			}
		}
	}
});
