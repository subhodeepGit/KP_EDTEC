frappe.listview_settings['Fees'] = {
	add_fields: ["grand_total", "outstanding_amount", "due_date","docstatus","return_issued"],
	get_indicator: function(doc) {
        if (flt(doc.outstanding_amount) > 0 && doc.docstatus==1 && doc.return_issued==1) {
			return [__("Return Issued"), "grey", "outstanding_amount,>,0"];
		}
		else if(flt(doc.outstanding_amount)==0) {
			return [__("Paid"), "green", "outstanding_amount,=,0"];
		} else if (flt(doc.outstanding_amount) > 0 && doc.due_date >= frappe.datetime.get_today()) {
			return [__("Unpaid"), "orange", "outstanding_amount,>,0|due_date,>,Today"];
		} else if (flt(doc.outstanding_amount) > 0 && doc.due_date < frappe.datetime.get_today()) {
			return [__("Overdue"), "red", "outstanding_amount,>,0|due_date,<=,Today"];
		}
        else if (flt(doc.outstanding_amount) < 0 && doc.docstatus==1) {
			return [__("Return"), "grey", "outstanding_amount,<,0"];
		}
	}
};