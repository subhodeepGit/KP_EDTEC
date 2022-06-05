frappe.ui.form.on('Fee Structure', {
	program(frm) {
        frm.clear_table("course_wise_fees");
        if (frm.doc.program){
                frappe.call({
                    method: "kp_edtec.ed_tec.doctype.fee_structure.get_courses",
                    args: {
                        program: frm.doc.program,
                    },
                    callback: function(r) { 
                        (r.message).forEach(element => {
                            var c = frm.add_child("course_wise_fees")
                            c.course=element.course
                        });
                        frm.refresh_field("course_wise_fees")
                    } 
                    
                });    
        }
	},
    setup(frm){
        frm.set_query("program",function(){
            return{
                filters:{
                    "programs":frm.doc.programs
                }
            }
        })
    },
  //   refresh(frm){
  //       frappe.call({
		// 	method: "ed_tec.ed_tec.doctype.fee_structure.get_fee_types",
		// 	callback: function(r) {
		// 		frm.set_df_property("fee_type", "options", r.message);
		// 	}
		// });
  //   }
})


frappe.ui.form.on("Fee Component", "fees_category", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.fees_category){
        var total_amount=0;
        (cur_frm.doc.course_wise_fees).forEach(e=>{
            total_amount+=(e.amount ? e.amount:0)
        })
        d.amount=total_amount;
        refresh_field("amount", d.name, d.parentfield);
    }
});