frappe.ui.form.on('Student Leave Application',{
    setup(frm){
        frm.set_query("student_group", function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.student_leave_application.get_group',
                filters: {
                    "student":frm.doc.student
                }
            };
        });
        frm.set_query("course_schedule", function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.student_leave_application.get_course_schedule',
                filters: {
                    "student":frm.doc.student
                }
            };
        });
    },
    // validate:function(frm){
    //     if(frm.doc.from_date  && frm.doc.to_date && frm.doc.from_date > frm.doc.to_date){
    //         frappe.throw("Start Date should be less than End Date");
    // }

//     if(frm.doc.from_date && frm.doc.from_date < frappe.datetime.get_today()){
//         frappe.throw("Start Date should be greater than today's date");
// }
//     }

})