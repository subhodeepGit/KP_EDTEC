// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Exam Block List', {
	setup:function(frm){
		frm.set_query("exam_declaration", function() {
			return {
				query: 'kp_edtec.ed_tec.doctype.student_exam_block_list.student_exam_block_list.get_declar',
				filters: {
					"disabled":0,
					"program_of_exam":frm.doc.program
				}
			};
		});
		
		frm.set_query("student","student_block_item", function() {
            return {
				query: 'kp_edtec.ed_tec.doctype.student_exam_block_list.student_exam_block_list.get_student_by_program',
                filters: {
                    "program":frm.doc.program
                }
            };
        });
		frm.set_query("semester", function() {
			var semesters=[];
			if (!frm.doc.exam_declaration){
				frappe.throw("Select Exam Declaration First")
			}
			return {
				filters: {
					"programs":frm.doc.program
				}
			};
		});

	},
});
frappe.ui.form.on("Student Block Item", "student", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if(d.student){
      
		frappe.call({
			method: "kp_edtec.ed_tec.doctype.student_exam_block_list.student_exam_block_list.get_student",
			args: {
				"student":d.student
			},
			callback: function(r) {
				d.student_name = r.message;				
				refresh_field("student_name", d.name, d.parentfield);
	
			}	
	});
 
    }
});