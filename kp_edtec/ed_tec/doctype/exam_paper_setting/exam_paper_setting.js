// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Exam Paper Setting', {
	assessment_plan: function(frm) {
		if (frm.doc.assessment_plan){
			frappe.call({
				method: "kp_edtec.ed_tec.doctype.exam_paper_setting.exam_paper_setting.get_assessment_plan_details",
				args: {
					assessment_plan: frm.doc.assessment_plan,
				},
				callback: function(r) { 
					(r.message).forEach(element => {
						frm.set_value('programs',element.programs)
						frm.set_value('program',element.program)
						frm.set_value('academic_year',element.academic_year)
						frm.set_value('academic_term',element.academic_term)
					});
				} 
				
			});   
		}
	},
	course: function(frm) {
		if (frm.doc.course){
			frappe.call({
				method: "kp_edtec.ed_tec.doctype.exam_paper_setting.exam_paper_setting.get_examiner_moderator",
				args: {
					course: frm.doc.course,
					assessment_plan:frm.doc.assessment_plan
				},
				callback: function(r) { 
					frm.set_value('examiner',(r.message).examiner)
					frm.set_value('moderator_name',(r.message).moderator)
				} 
			});   
		}
	},
	schedule_date:function(frm){
		if (frm.doc.schedule_date &&  frm.doc.schedule_date < frappe.datetime.get_today()){
			frappe.throw("Please select date after today's date for Schedule Date");

		}
	},
	validate:function(frm){
		if(frm.doc.from_time && frm.doc.to_time && frm.doc.from_time > frm.doc.to_time){
				frappe.throw("To time should be greater than From time");
		}

	},

	setup:function(frm){
		frm.set_query("program", function() {
            return {
                filters: {
                    "programs":frm.doc.programs
                }
            };
        });
		frm.set_query("academic_term", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year
                }
            };
        });
		frm.set_query("course", function() {
            // return {
            //     filters: {
            //         "program":frm.doc.program
            //     }
            // };
            return {
				query: 'kp_edtec.ed_tec.doctype.exam_paper_setting.exam_paper_setting.filter_course',
				filters: {
					"assessment_plan":frm.doc.assessment_plan
				}
			};
        });
        frm.set_query("assessment_plan", function() {
			return {
				filters: {
					"docstatus": 1
				}
			};
		});
        frm.set_query("examiner", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.exam_paper_setting.exam_paper_setting.filter_examiner',
				filters: {
					"assessment_plan":frm.doc.assessment_plan,
					"course":frm.doc.course
				}
			};
		});
		frm.set_query("moderator_name", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.exam_paper_setting.exam_paper_setting.filter_moderator',
				filters: {
					"assessment_plan":frm.doc.assessment_plan,
					"course":frm.doc.course
				}
			};
		});
		frm.set_df_property('examiner', 'reqd', 1);
		frm.set_df_property('programs', 'reqd', 1);
		frm.set_df_property('program', 'reqd', 1);
		frm.set_df_property('course', 'reqd', );
		frm.set_df_property('paper_copy', 'reqd', 1);
		
	}
});
