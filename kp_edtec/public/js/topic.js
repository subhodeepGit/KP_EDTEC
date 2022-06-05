frappe.ui.form.on('Topic',{
    refresh: function(frm) {
        if (frappe.user.has_role(["Student","Instructor"]) && !frappe.user.has_role(["System Manager"]) ){
            frm.remove_custom_button("Add to Courses","Action");
        }
    }
        
})