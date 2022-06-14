// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Exam Declaration', {
    refresh: function(frm){
        if(frm.doc.docstatus == 1 && frappe.user.has_role(["System Manager"])){
            frm.add_custom_button("Exam Assessment Plan", () => {
                let data = {}
                data.programs = frm.doc.exam_program
                data.program = frm.doc.program
                data.academic_year = frm.doc.academic_year
                data.academic_term = frm.doc.academic_term
                data.exam_declaration = frm.doc.name
                frappe.new_doc("Exam Assessment Plan", data)
            },__('Create'));

            frm.add_custom_button("Student Group", () => {
                let data = {}
                data.group_based_on = frm.doc.doctype
                data.programs = frm.doc.exam_program
                data.program = frm.doc.program
                data.academic_year = frm.doc.academic_year
                data.academic_term = frm.doc.academic_term
                data.exam_declaration = frm.doc.name
                frappe.new_doc("Student Group", data)
            },__('Create'));

            if(frm.doc.is_application_required){
                frm.add_custom_button("Student Admit Card", () => {
                    frappe.call({
                        method: 'create_student_admit_card',
                        doc:frm.doc,
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint("Student Admit Card Created")
                            }
                        }
                    });
                },__('Create')); 
            }
        }
    
    
 
		// if (!frm.doc.__islocal){
		// 	frm.add_custom_button(__('Create Fees'), function() {
		// 		frappe.call({
		// 			method: 'make_exam_assessment_result',
        //             // /opt/bench/frappe-bench/apps/kp_edtec/kp_edtec/kp_edtec/doctype/exam_declaration/exam_declaration.py
		// 			doc: frm.doc,
		// 			callback: function() {
		// 				frm.refresh();
		// 			}
		// 		});
		// 	}).addClass('btn-primary');;
		// }
		
	
    },
    setup:function(frm){
        frm.set_query('program', function(doc) {
			return {
				filters: {
					"programs":frm.doc.exam_program
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
        frm.set_query('fee_structure', 'fee_structure', function() {
		    return {
				filters: {
					"programs":frm.doc.exam_program,
                    "docstatus":1
				}
			};
		});
  //       frm.set_query("course_assessment_plan", function() {
  //           var semesters = cur_frm.doc.semesters.map(d => d.semester);
		// 	return {
		// 		filters: {
		// 			"programs":frm.doc.exam_program,
  //                   "program":["in", semesters],
		// 			"academic_year":frm.doc.academic_year,
  //                   "docstatus":1
		// 		}
		// 	};
		// });
        frm.set_query('semester', 'semesters', function() {
		    return {
				filters: {
					"programs":frm.doc.exam_program
				}
			};
		});
        frm.fields_dict['fee_structure'].grid.get_field("fee_structure").get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    "fee_type": "Exam Fees",
                    "programs":frm.doc.exam_program
                }
            }
        }
        frm.fields_dict['courses_offered'].grid.get_field("courses").get_query = function(doc, cdt, cdn) {
            var semesters = cur_frm.doc.semesters.map(d => d.semester);
            return {
                query: 'kp_edtec.kp_edtec.doctype.exam_declaration.exam_declaration.filter_courses',
                filters: {
                    "program":semesters
                }
            };
        }
        
    },
	get_courses: function(frm) {
		frm.clear_table("courses_offered");
        frappe.call({
            method: 'get_courses',
            doc: frm.doc,
            callback: function(r) {
                if (r.message) {
                    (r.message).forEach(element => {
                        var c = frm.add_child("courses_offered")
                        c.courses = element.name
                        c.course_code = element.course_code
                        c.course_name = element.course_name
                        c.semester = element.semester
                    });
                    frm.refresh_field("courses_offered")
                }
            }
        });
	},
 
    get_students:function(frm){
		frm.clear_table("students");
		frappe.call({
			method: "kp_edtec.kp_edtec.doctype.exam_declaration.exam_declaration.get_students",
			args: {
				programs: frm.doc.exam_program,
				academic_term: frm.doc.academic_term
			},
			callback: function(r) {
				
				(r.message).forEach(element => {
					var row = frm.add_child("students")
					row.student=element.student
					row.student_name=element.student_name
                    row.roll_no = element.roll_no
                    row.registration_number = element.registration_number
				});
				frm.refresh_field("students")
                frm.save();
				frm.set_value("total_enrolled_student",(r.message).length)
			}
			
		});
	}
}); 



frappe.ui.form.on("Exam Declaration Fee Item",{
    fee_structure: function(frm,cdt,cdn){
        var row = locals[cdt][cdn]
        frappe.db.get_value("Fee Structure", {'name':row.fee_structure,  "docstatus":1},'total_amount', resp => {
            row.amount = resp.total_amount
            frm.refresh_fields(row.amount)
        })
    }
})
// frappe.ui.form.on('Exam Declaration', {
//     refresh: function(frm) {
// 		if(frm.doc.docstatus > 0) {
// 			frm.add_custom_button(__('Accounting Ledger'), function() {
// 				frappe.route_options = {
// 					voucher_no: frm.doc.name,
// 					from_date: frm.doc.posting_date,
// 					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
// 					company: frm.doc.company,
// 					group_by: '',
// 					show_cancelled_entries: frm.doc.docstatus === 2
// 				};
// 				frappe.set_route("query-report", "General Ledger");
// 			}, __("View"));
// 		}
// 	}
// })
