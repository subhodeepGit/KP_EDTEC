import frappe

def execute():
    update_employee_permission()


def update_employee_permission():
    for emp in frappe.get_all("Employee"):
        employee=frappe.get_doc("Employee",emp.name)
        employee.save()