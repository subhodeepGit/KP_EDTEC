// Copyright (c) 2021, suraj varade and contributors
// For license information, please see license.txt
frappe.ui.form.on('Room Type', {
	setup:function(frm){
        frm.set_query("fees_structure", function() {
			return {
				filters:{
					"fee_type":"Hostel Fees"
				}
			};
		});
	},
	capacity:function(frm){
        if(frm.doc.capacity){
        	frappe.call({
				method:"set_capacity",
				doc: frm.doc
		  })
        }
	},
	amenity_template: function(frm) {
		if(frm.doc.amenity_template){
			frappe.model.with_doc("Hostel Amenity Template", frm.doc.amenity_template, function() {
	            var tabletransfer= frappe.model.get_doc("Hostel Amenity Template", frm.doc.amenity_template)
	            frm.clear_table("amenity_list");
	            $.each(tabletransfer.amenity_list, function(index, row){
	                var d = frm.add_child("amenity_list");
	                d.amenity = row.amenity;
	                frm.refresh_field("amenity_list");
	            });
	        });
        }
	}
});
