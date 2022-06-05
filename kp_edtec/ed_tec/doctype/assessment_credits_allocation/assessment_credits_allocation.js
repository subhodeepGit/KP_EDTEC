// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assessment Credits Allocation', {
	setup: function(frm) {
		frm.set_query("student", function() {
			return {
				filters: {
					"enabled":1
				}
			};
		});
		frm.set_query("course", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.assessment_credits_allocation.assessment_credits_allocation.get_courses',
				filters: {
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("assessment_criteria", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.assessment_credits_allocation.assessment_credits_allocation.get_assessment_criteria',
				filters: {
					"course":frm.doc.course,
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year,
				}
			};
		});
	},
	refresh:function(frm){
		frm.set_df_property('final_credit_item', 'cannot_add_rows', true);
	},
	get_assessments:function(frm){
		if(frm.doc.assessment_criteria){
			frappe.call({
				method:"kp_edtec.ed_tec.doctype.assessment_credits_allocation.assessment_credits_allocation.get_course_assessment",
				args: {
					student:frm.doc.student,
					course:frm.doc.course,
					assessment_criteria	:frm.doc.assessment_criteria
				},
				callback: function(r) {
					if (r.message){
						console.log("wwww r.message",r.message)
						frm.clear_table("final_credit_item");
						$.each(r.message || [], function(i, d) {
							var row=frm.add_child("final_credit_item")
							row.course_assessment=d.name
							row.earned_marks=d.earned_marks
							row.total_marks=d.total_marks
							frm.set_value("weightage_marks",d.weightage_marks)
						})
						frm.refresh_field("final_credit_item")
					}
				}
		    })
		}
		else{
			frappe.msgprint("Please fill the assessment criteria first.")
		}
		
	},
	student:function(frm){
		if (frm.doc.student){
			frappe.db.get_doc("Student",frm.doc.student).then(( resp ) => {
				(resp.current_education).forEach((  row ) => {
					frm.set_value("academic_year",row.academic_year)
					frm.set_value("academic_term",row.academic_term)
				})
			});
		}
	},
	course:function(frm){
		frm.trigger("get_course_details")
	},
	assessment_criteria:function(frm){
		frm.trigger("get_course_details")
	},
	get_course_details:function(frm){
		if (frm.doc.course && frm.doc.assessment_criteria){
			frappe.call({
				method:"get_course_details",
				doc: frm.doc,
				callback: function(r) {
					if (r.message){
						frm.set_value("total_credits",r.message['credits'])
						frm.set_value("earned_credits",r.message['credits'])
						frm.set_value("out_of_marks",r.message['total_marks'])
					}
				}
		  })
		}
		if (frm.doc.course && frm.doc.assessment_criteria){
			frappe.call({
				method: 'kp_edtec.ed_tec.doctype.exam_assessment_plan.exam_assessment_plan.get_assessment_criteria_detail',
				args: {
					course:frm.doc.course,
					criteria:frm.doc.assessment_criteria
				},
				callback: function(r) {
					if (r.message){
						frm.set_value("out_of_marks",r.message['total_marks'])
					}
				}
			});
		}
		
	}
});
