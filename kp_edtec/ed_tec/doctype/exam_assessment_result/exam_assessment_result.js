// Copyright (c) 2022, suraj varade and contributors
// For license information, please see license.txt
frappe.ui.form.on('Exam Assessment Result', {
	refresh: function(frm) {
		if (!frm.doc.__islocal) {
			frm.trigger('setup_chart');
		}
		frm.set_df_property('details', 'read_only', 1);
        frm.set_query('program', function(doc) {
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
		frm.set_query('course', function() {
			return {
				query: 'erpnext.education.doctype.program_enrollment.program_enrollment.get_program_courses',
				filters: {
					'program': frm.doc.program
				}
			};
		});

		frm.set_query('course','assessment_result_item', function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.exam_assessment_result.exam_assessment_result.filter_courses',
				filters: {
					'student': frm.doc.student
				}
			};
		});
		frm.set_query('academic_term', function() {
			return {
				filters: {
					'academic_year': frm.doc.academic_year
				}
			};
		});
	},
	setup:function(frm){
		// frm.set_query("student", function() {
		// 	return {
		// 		query: 'ed_tec.ed_tec.doctype.student_group.filter_student',
		// 		filters: {
		// 			"student_group":frm.doc.student_group
		// 		}
		// 	};
		// });
		if(frm.doc.student){
    		frm.set_query("programs", function() {
                return {
                    query: 'kp_edtec.ed_tec.doctype.fees.get_progarms',
                    filters: {
                        "student":frm.doc.student
                    }
                };
            });
    	}

    },
    student:function(frm){
    	if(frm.doc.student){
	    	frappe.call({
				method: "kp_edtec.ed_tec.doctype.exam_assessment_result.exam_assessment_result.get_student_details",
				args: {
					student:frm.doc.student,
				},
				callback: function(r) { 
					if(r.message){
						frm.set_value("programs",r.message.programs)
						frm.set_value("program",r.message.program)
						frm.set_value("academic_year",r.message.academic_year)
						frm.set_value("academic_term",r.message.academic_term)
					}
				} 
			});
	    }
	    else{
	    	frm.set_value("student_name",'')
	    	frm.set_value("programs",'')
			frm.set_value("program",'')
			frm.set_value("academic_year",'')
			frm.set_value("academic_term",'')
			frm.set_value("assessment_status",'')
	    }
    },
    get_result:function(frm){
    	if(frm.doc.student && frm.doc.academic_year && frm.doc.academic_term){
			frappe.call({
				method: "set_assessment_result_item",
				doc: frm.doc,
				callback: function() {
	                frm.refresh();
	                frappe.call({
						method: "kp_edtec.ed_tec.doctype.exam_assessment_result.exam_assessment_result.get_assessment_status",
						args: {
							student:frm.doc.student,
							semester: frm.doc.program,
							academic_year: frm.doc.academic_year,
							academic_term: frm.doc.academic_term,
						},
						callback: function(r) { 
							if(r.message){
								frm.set_value("assessment_status","Completed")
							}
							else{
								frm.set_value("assessment_status","Pending")
							}
						} 
					});
				}
			});
		}
		else if(!frm.doc.student){
			frappe.msgprint("Please select student")
		}
		else if(!frm.doc.academic_year){
			frappe.msgprint("Academic year missing in course enrollment of student")
		}
		else if(!frm.doc.academic_term){
			frappe.msgprint("Academic term missing in course enrollment of student")
		}
	},
	setup_chart: function(frm) {
		let labels = [];
		let maximum_scores = [];
		let scores = [];
		if (labels.length && maximum_scores.length && scores.length) {
			frm.dashboard.chart_area.empty().removeClass('hidden');
			new frappe.Chart('.form-graph', {
				title: 'Course Assessment Results',
				data: {
					labels: labels,
					datasets: [
						{
							name: 'Maximum Score',
							chartType: 'bar',
							values: maximum_scores,
						},
						{
							name: 'Score Obtained',
							chartType: 'bar',
							values: scores,
						}
					]
				},
				colors: ['#4CA746', '#98D85B'],
				type: 'bar'
			});
		}
	}
});

frappe.ui.form.on("Assessment Result Item", "score", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.credit_score=((d.credit||0)*(d.score||0))
	refresh_field("credit_score", d.name, d.parentfield);
});
frappe.ui.form.on("Assessment Result Item", "practical_obtained_marks", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.score=((d.theory_obtained_marks||0)+(d.practical_obtained_marks||0))
	refresh_field("maximum_score", d.name, d.parentfield);
	d.credit_score=((d.credit||0)*(d.score||0))
	refresh_field("credit_score", d.name, d.parentfield);
});
frappe.ui.form.on("Assessment Result Item", "theory_obtained_marks", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.score=((d.theory_obtained_marks||0)+(d.practical_obtained_marks||0))
	refresh_field("maximum_score", d.name, d.parentfield);
	d.credit_score=((d.credit||0)*(d.score||0))
	refresh_field("credit_score", d.name, d.parentfield);
});