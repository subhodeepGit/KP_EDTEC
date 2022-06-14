import frappe

@frappe.whitelist()
def get_courses(program):
    return frappe.db.sql('''select course from `tabProgram Course` where parent = %s and required = 1''', (program), as_dict=1)

@frappe.whitelist()
def get_fee_types():
    types=[]
    for d in frappe.get_all("Fee Type",order_by="name"):
        types.append(d.name)
    return "\n".join([''] + types)
