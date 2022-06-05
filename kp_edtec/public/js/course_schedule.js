frappe.ui.form.on('Course Schedule', {
    setup(frm){
        frm.set_query("course", function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.course_schedule.get_courses_from_student_group_semester',
                filters: {
                    "student_group":frm.doc.student_group,
                    "instructor":frm.doc.instructor
                }
            };
        });
        frm.set_query("instructor", function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.course_schedule.get_instructor_by_student_group',
                filters: {
                    "student_group":frm.doc.student_group
                }
            };
        });
        frm.set_query("exam_declaration", function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.course_schedule.get_exam_declaration_by_course',
                filters: {
                    "course":frm.doc.course
                }
            };
        });
        frm.set_query("student","student_paper_code",function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.course_schedule.get_student_by_student_group',
                filters: {
                    "student_group":frm.doc.student_group
                }
            };
        });
        frm.set_query("instructor", "additional_instructor", function() {
            return {
                query: 'kp_edtec.ed_tec.doctype.course_schedule.get_instructor',
                filters:{"course":frm.doc.course,"student_group":frm.doc.student_group}
            };
        });
    },
    refresh(frm){
        if (frappe.user.has_role(["Student"]) && !frappe.user.has_role('System Manager')){
            frm.remove_custom_button("Mark Attendance");
        }
    },
    // student_group(frm){
    //     frm.set_value("instructor",'');
    //     frm.set_value("instructor_name",'');
    //     frm.set_value("additional_instructor",'');
    //     frm.set_value("room",'');
    //     frm.set_value("schedule_date",'');
    //     frm.set_value("from_time",'');
    //     frm.set_value("to_time",'');
    //     frappe.db.get_value("Student Group", {'name':frm.doc.student_group},['class_room','exam_schedule_date','from_time','to_time', 'group_based_on','exam_declaration'], resp => {
    //         frm.set_value("room",resp.class_room);
    //         if (resp.exam_schedule_date){
    //             frm.set_value("schedule_date",resp.exam_schedule_date);
    //         }
    //         if (resp.from_time){
    //             frm.set_value("from_time",resp.from_time);
    //         }
    //         if (resp.to_time){
    //             frm.set_value("to_time",resp.to_time);
    //         }
    //         if(resp.group_based_on == 'Exam Declaration'){
    //             frm.set_value("is_exam_schedule",1);
    //             frm.set_value("exam_declaration",resp.exam_declaration);
    //         }
    //     })

    // },
    course(frm){
        if (!frm.doc.course){
            frm.set_value("course_name",'');
            frm.set_value("course_code",'');
        }
    }
})