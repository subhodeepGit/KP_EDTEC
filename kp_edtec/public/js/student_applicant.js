frappe.ui.form.on('Student Applicant', {
  
    onload: function(frm) {
        frm.set_query("counselling_structure", function() {
            return {
                filters: {
                    "program_grade":frm.doc.program_grade,
                    "academic_year":frm.doc.academic_year
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
        frm.fields_dict['program_priority'].grid.get_field('programs').get_query = function(doc, cdt, cdn) {
            return {   
                query: 'kp_edtec.ed_tec.doctype.student_applicant.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.department,
                    "program_grade":frm.doc.program_grade
                }
            }
        }
        frm.set_query("department", function(){
	        return{
	            filters:{
	                "is_group":1,
	                "is_stream": 1
	            }
	        }
	    });
        

    },
    states(frm){
        frm.set_value("country_code",'')
        frappe.db.get_value('State',{'name':frm.doc.states},['country'],(val1) =>
        {
            frappe.db.get_value('Country',{'name':val1.country},['country_phone_code'],(val2) =>
            {
                frm.set_value("country_code",val2.country_phone_code)
            })
        })
    },
    after_save: function(frm) {
        frm.trigger("hide_n_show_child_table_fields");
    },
    setup: function(frm) {
        frm.set_query("blocks", function() {
            return {
                filters: {
                    "districts":frm.doc.districts
            }
        };
        
    });

        frm.set_query("districts", function() {
            return {
                filters: {
                    "state":frm.doc.state
                }
            };
        });
      
    },
   
    hide_n_show_child_table_fields(frm){
        var df = frappe.meta.get_docfield("Education Qualifications Details","qualification_", frm.doc.name);
        df.hidden = 1
        var df0 = frappe.meta.get_docfield("Education Qualifications Details","qualification", frm.doc.name);
        df0.hidden = 0
        var df1 = frappe.meta.get_docfield("Education Qualifications Details","year_of_completion_", frm.doc.name);
        df1.hidden = 1
        var df11 = frappe.meta.get_docfield("Education Qualifications Details","year_of_completion", frm.doc.name);
        df11.hidden = 0
        var df2 = frappe.meta.get_docfield("Document List","document_name_", frm.doc.name);
        df2.hidden = 1
        var df4 = frappe.meta.get_docfield("Document List","document_name", frm.doc.name);
        df4.hidden = 0
        var df5 = frappe.meta.get_docfield("Document List","attach", frm.doc.name);
        var df6 = frappe.meta.get_docfield("Document List","attached", frm.doc.name);
        if(df5!=null){
            df6.default = 0
        }
    },
   
    before_load: function(frm) {
        frm.trigger("hide_n_show_child_table_fields");
      
    },
    refresh(frm){
        

        frm.set_df_property('education_qualifications_details', 'cannot_add_rows', true);
        frm.set_df_property('education_qualifications_details', 'cannot_delete_rows', true);
        frm.set_df_property('document_list', 'cannot_add_rows', true);
        frm.set_df_property('document_list', 'cannot_delete_rows', true);
        if (cur_frm.doc.document_list){
            cur_frm.doc.document_list.forEach(data=>{
                var dn = frappe.meta.get_docfield("Document List", "document_name",data.name);
                dn.read_only=1;
                // var m = frappe.meta.get_docfield("Document List", "mandatory",data.name);
                // m.read_only=1;
                // var ms = frappe.meta.get_docfield("Document List", "is_available",data.name);
                // m.read_only=1;
            })
        }
        frm.set_df_property('program', 'hidden', 1);
        frm.set_df_property('programs_', 'hidden', 1);
        frm.set_df_property('student_admission', 'hidden', 1);
        frm.remove_custom_button("Enroll")
        if (!cur_frm.doc.__islocal && frappe.user.has_role(["Student"]) && !frappe.user.has_role(["System Manager"])){
            frm.remove_custom_button("Reject","Actions");
            frm.remove_custom_button("Approve","Actions");
            
        }
        if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role(["System Manager"])){
            frm.set_df_property('application_status', 'read_only', 1);
        }
        if (frm.doc.application_status === "Approved" && frm.doc.docstatus === 1) {
            frappe.db.get_value('User',{'name':frappe.session.user},['module_profile'],(val) =>
			{
                if (val.module_profile!="Student"){
                    console.log("............1")
                    frm.trigger("show_fees_button")
                    frappe.db.get_list("Program Enrollment", {
                        filters:{"reference_doctype":"Student Applicant","reference_name":frm.doc.name},
                        fields: ["name"]
                    }).then((data) => { 
                        if (data.length==0) 
                        frm.add_custom_button(__("Enroll"), function() {
                            frm.trigger("enroll_student")
                        }).addClass("btn-primary");
                    })
                }
				
			});
			
        }
        frappe.call({
            method: "kp_edtec.ed_tec.doctype.student_applicant.get_qualification_list",
            callback: function(r) {
                cur_frm.doc.education_qualifications_details.forEach(data=>{
                    var df = frappe.meta.get_docfield("Education Qualifications Details","qualification_", data.name);
                    df.options = r.message.qual;
                    var df1 = frappe.meta.get_docfield("Education Qualifications Details","year_of_completion_", data.name);
                    df1.options = r.message.acadmic;
                })
            }
        });
        
        // set Sharing Types 
        frappe.call({
            method: "kp_edtec.ed_tec.doctype.student_applicant.get_sharing_type",
            callback: function(r) {
                frm.set_df_property('sharing', 'options', r.message);
            }
        }); 
  
        // clear education qualification details table

        // if (frm.doc.__islocal){
        //     frm.set_value("education_qualifications_details",[]);
        //     // frm.set_value("student_category","")
        // }      

    },

    counselling_structure: function(frm) {
        frm.trigger("get_education_and_document_list");
        frm.set_value("document_list",[]);
    },
    enroll_student: function(frm) {
		frappe.model.open_mapped_doc({
			method: "kp_edtec.ed_tec.doctype.student_applicant.enroll_student",
			frm: frm
		})
	},
    show_fees_button(frm){
        if (frm.doc.name && frm.doc.application_status=="Approved"){
            frm.add_custom_button(__("Fees"), function() {
                frappe.model.open_mapped_doc({
                    method: "kp_edtec.ed_tec.doctype.student_applicant.create_fees",
                    frm: frm,
                });
            })
    }
},
    program_grade(frm){
        // frm.trigger("get_counselling_structure");
        frm.set_value("counselling_structure",'')
        frm.set_value("program_priority",[]);
        frm.trigger("get_qualification_detail_for_admission");
        
    },
    academic_year(frm){
        // frm.trigger("get_counselling_structure");
        frm.set_value("program_priority",[]);
        frm.set_value("counselling_structure",'')
        frm.set_value("counselling_structure",'');
    },
    department(frm){
        // frm.trigger("get_counselling_structure");
        frm.set_value("counselling_structure",'')
        frm.set_value("program_priority",[]);
    },
    student_category(frm){
        frm.trigger("get_education_and_document_list");
    },
    
    // get_counselling_structure(frm){
    //     frm.set_value("counselling_structure",'');
    //     if (frm.doc.program_grade && frm.doc.academic_year && frm.doc.department){
    //         frappe.call({
    //             method: "ed_tec.ed_tec.doctype.student_applicant.get_counselling_structure",
    //             args:{
    //                program_grade: frm.doc.program_grade,
    //                academic_year: frm.doc.academic_year,
    //                department: frm.doc.department
    //             },
    //             callback: function(r) { 
    //                 if (r.message){
    //                    frm.set_value("counselling_structure",r.message['name']);
    //                 }
    //             } 
    //         });
    //     }
        
    // },
    get_education_and_document_list(frm){
        frm.set_value("education_qualifications_details",[]);
        if (frm.doc.counselling_structure && frm.doc.student_category){
            frappe.model.with_doc("Counselling Structure", frm.doc.counselling_structure, function() {
                var tabletransfer= frappe.model.get_doc("Counselling Structure", frm.doc.counselling_structure)
                $.each(tabletransfer.eligibility_parameter_list, function(index, row){
                    if(frm.doc.student_category == row.student_category){
                        var d = frm.add_child("education_qualifications_details");
                        d.qualification = row.parameter;
                        d.percentage_cgpa = row.percentagecgpa
                    }
                    frm.refresh_field("education_qualifications_details");
                });
                $.each(tabletransfer.counselling_fees, function(index, row){
                    if(frm.doc.student_category == row.student_category){
                        frm.set_value("total_counselling_fee",row.amount)
                    }
                    frm.refresh_field("total_counselling_fee");
                });
            });
        }
       
    },
    get_qualification_detail_for_admission(frm){
        if (!frm.doc.counselling_structure && frm.doc.student_category && (frm.doc.program_priority).length!=0){
            frm.set_value("education_qualifications_details",[]);
            frappe.call({
                method: "kp_edtec.ed_tec.doctype.student_applicant.get_education_qualifications_details_by_admissions",
                args:{
                    student_category: frm.doc.student_category,
                    admission:  frm.doc.program_priority
                },
                callback: function(resp) { 
                    if (resp.message){
                        $.each(resp.message, function(index, row){
                                var edu_row = frm.add_child("education_qualifications_details");
                                edu_row.qualification = row.parameter;
                                edu_row.percentage_cgpa = row.percentagecgpa
                            frm.refresh_field("education_qualifications_details");
                        });
                    }
                } 
            });
        }
    }
})
frappe.ui.form.on("Education Qualifications Details", "earned_marks", function(frm, cdt, cdn) {
       
    var data = locals[cdt][cdn];

    if(data.total_marks>=data.earned_marks){
        data.total_marks==" " && data.earned_marks==" "
        data.score=(data.earned_marks/data.total_marks)*100
    }
    else{
        frappe.throw("Please Enter Valid Data..")
    }       
    cur_frm.refresh_field ("education_qualifications_details");
 
 });	

 frappe.ui.form.on("Education Qualifications Details", "cgpa", function(frm, cdt, cdn) {
  
    var data = locals[cdt][cdn];
    if(data.cgpa<=10 && data.cgpa>=0){
        data.score=data.cgpa*10   
    }
    else if(data.cgpa>10 || data.cgpa<0){
        frappe.throw("Please enter your valid CGPA")
    }
    else{
        frappe.throw("Wrong Entry")
    }
    
    cur_frm.refresh_field ("education_qualifications_details");
 
 });       
frappe.ui.form.on("Program Priority", "programs", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
   
    frappe.model.set_value(cdt, cdn, "student_admission",'');
    frappe.model.set_value(cdt, cdn, "semester", '');
    frm.set_value("counselling_structure",'')
    frm.set_value("program",'')
    if (!frm.doc.program_grade){
        frappe.msgprint("Please Fill Program Grade First")
        d.programs=''
    }
    if (!frm.doc.academic_year){
        frappe.msgprint("Please Fill Academic Year First")
        d.programs=''
    }
    if (!frm.doc.student_category){
        frappe.msgprint("Please Fill Student First")
        d.programs=''
    }
    if (d.programs){
        frappe.call({
            method: "kp_edtec.ed_tec.doctype.student_applicant.get_admission_and_semester_by_program",
            args: {
               programs:d.programs,
               program_grade:frm.doc.program_grade,
               academic_year:frm.doc.academic_year
            },
            callback: function(r) { 
                if (r.message){
                    if (r.message["no_record_found"]){
                        frappe.msgprint("Admission Not Declared for this program")
                        frappe.model.set_value(cdt, cdn, "programs",'');
                    }
                    frm.set_value("program",r.message['semester'])
                    frm.set_value("programs_",r.message['admission_program'])
                    frappe.model.set_value(cdt, cdn, "student_admission", r.message['name']);
                    frappe.model.set_value(cdt, cdn, "semester", r.message['semester']);
                    if (r.message['counselling_required']){
                        frm.set_value("counselling_structure",r.message['counselling_structure'])
                    }
                    if (!frm.doc.counselling_structure && frm.doc.student_category && (frm.doc.program_priority).length!=0){
                        frm.set_value("education_qualifications_details",[]);
                        frappe.call({
                            method: "kp_edtec.ed_tec.doctype.student_applicant.get_education_qualifications_details_by_admissions",
                            args:{
                                student_category: frm.doc.student_category,
                                admission:  frm.doc.program_priority
                            },
                            callback: function(resp) { 
                                if (resp.message){
                                    $.each(resp.message, function(index, row){
                                            var edu_row = frm.add_child("education_qualifications_details");
                                            edu_row.qualification = row.parameter;
                                            edu_row.percentage_cgpa = row.percentagecgpa
                                        frm.refresh_field("education_qualifications_details");
                                    });
                                }
                            } 
                        });
                    }
                }
            } 
        }); 
    }
});
