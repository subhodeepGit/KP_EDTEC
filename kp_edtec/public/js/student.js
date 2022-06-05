frappe.ui.form.on('Student',{
    refresh: function(frm) {
        if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role('System Manager')){
            frm.remove_custom_button("Accounting Ledger");
        } 
    }
})