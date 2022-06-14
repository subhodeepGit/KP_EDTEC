frappe.ui.form.on('Student Log',{
    setup: function(frm) {
        frm.set_query("academic_term", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year
                }
            };
        });
        frm.set_query("program", function() {
            return {
                query: 'kp_edtec.kp_edtec.doctype.student.get_sem',
                filters: {
                    "student":frm.doc.student
                }
            };
        });
        frm.set_query("student_batch", function() {
            return {
                query: 'kp_edtec.kp_edtec.doctype.student.get_batch',
                filters: {
                    "student":frm.doc.student
                }
            };
        });
    }
})