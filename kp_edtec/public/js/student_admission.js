frappe.ui.form.on('Student Admission', {
    before_save(frm){
        if(frm.doc.admission_start_date && frm.doc.admission_end_date && frm.doc.admission_end_date < frm.doc.admission_start_date){
            
            frappe.throw("Counselling End date should be greater than Counselling Start date");
        
        }
        if(frm.doc.enrollment_end_date && frm.doc.enrollment_start_date && frm.doc.enrollment_end_date < frm.doc.enrollment_start_date){
            
            frappe.throw("Enrollment End date should be greater than Enrollment Start date");
        
        }
    },
    setup(frm) {
        frm.set_df_property('program_grade', 'reqd', 1);
        frm.set_query("academic_calendar", function() {
            return {
                filters: {
                    "programs":frm.doc.admission_program,
                    "program":frm.doc.semester
                }
            };
        });
        frm.set_query("counselling_structure", function() {
            return {
                query: 'kp_edtec.kp_edtec.doctype.student_admission.get_counselling_structure',
                filters: {
                    "program_grade":frm.doc.program_grade,
                    "programs":frm.doc.admission_program,
                    "academic_year":frm.doc.academic_year
                }
            };
        });
        frm.set_query("admission_program", function() {
            return {
                filters: {
                    "program_grade":frm.doc.program_grade
                }
            };
        });
        frm.set_query("fee_structure","hostel_fees_", function(){
            return{
                filters:{
                    "programs":frm.doc.admission_program,
                    "docstatus":1
                }
            }
        })
        frm.set_query("fee_structure","counselling_fee_structures", function(){
            return{
                filters:{
                    "fee_type":"Counselling Fees",
                    "programs":frm.doc.admission_program ,
                    "docstatus":1
                }
            }
        })
        frm.set_query("fee_structure","admission_fee_structure", function(){
            return{
                filters:{
                    "fee_type":"Admission Fees",
                    "programs":frm.doc.admission_program,
                    "docstatus":1
                }
            }
        })
		frm.set_query("semester", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.student_admission.get_sem',
				filters: {
					"program":frm.doc.admission_program
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
        frm.set_query("document_type","reservations_distribution", function(){
            return{
                query: 'kp_edtec.kp_edtec.doctype.student_admission.get_doc'
            }
        })
        frm.fields_dict['reservations_distribution'].grid.get_field('seat_reservation_type').get_query = function(doc){
            let seat_reservation_type_list = [];
            if(!doc.__islocal) seat_reservation_type_list.push(doc.seat_reservation_type);
            $.each(doc.reservations_distribution, function(idx, val){
                if (val.seat_reservation_type) seat_reservation_type_list.push(val.seat_reservation_type);
            });
            return { filters: [['Seat Reservation Type', 'name', 'not in', seat_reservation_type_list]] };
        };
        // frm.fields_dict['required_documents_list'].grid.get_field('student_category').get_query = function(doc){
        //     let document_type_list = [];

        //     // if(!doc.__islocal) document_type_list.push(doc.document_type, doc.student_category);
        //     console.log("000000000document_type_list ",document_type_list)
        //     $.each(doc.required_documents_list, function(idx, val){

        //         if (val.document_type) document_type_list.push({'document_type':val.document_type});
        //         if (val.student_category) document_type_list.push({'student_category':val.student_category});
        //     });
        //     console.log("1111111document_type_list ",document_type_list)
           
        //     return { filters: [['Documents Template', 'name', 'in', document_type_list],['Student Category', 'name', 'not in', document_type_list],['Documents Template', "is_active","=",1]] };
        // };
         frm.set_query("document_type","required_documents_list", function() {
            return {
                filters: {
                    "is_active":1
                }
            };
        });

    }
})


frappe.ui.form.on("Reservations List", "update_balance", function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        let dialog = new frappe.ui.Dialog({
        title: __('Update Seats'),
        fields: [
            {
                "label" : "Type",
                "fieldname": "type",
                "fieldtype": "Select",
                "options":"\nAdd Balance\nDeduct Balance",
                "reqd":1
            },
            {
                "label" : "No of Seats",
                "fieldname": "no_of_seats",
                "fieldtype": "Int"
            }
        ],
        primary_action: function() {
            var data=dialog.get_values();
            if (data.type=="Add Balance"){
                frappe.model.set_value(cdt, cdn, "allocated_seat", (d.allocated_seat || 0)+data.no_of_seats);
                frappe.model.set_value(cdt, cdn, "seat_balance", (d.seat_balance || 0)+data.no_of_seats);
            }
            else{
                frappe.model.set_value(cdt, cdn, "allocated_seat", (d.allocated_seat || 0)-data.no_of_seats);
                frappe.model.set_value(cdt, cdn, "seat_balance", (d.seat_balance || 0)-data.no_of_seats);
            }
            dialog.hide();
        },
        primary_action_label: __('Update')
        });
        dialog.show();
       
});
frappe.ui.form.on("Eligibility Parameter List", "percentagecgpa", function(frm, cdt, cdn) {
    frappe.model.set_value(cdt, cdn, "total_score", 0);
    frappe.model.set_value(cdt, cdn, "eligible_score", 0);
});
frappe.ui.form.on("Required Documents", "document_type", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    frappe.db.get_value("Documents Template", {'name':d.document_type},'student_category', resp => {
        frappe.model.set_value(cdt, cdn, "student_category", resp.student_category);
    })
});