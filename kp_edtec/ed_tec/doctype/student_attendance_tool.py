import frappe

@frappe.whitelist()
def get_student_records(building,hostel_room=None):
    student_list=[]
    count=1
    fltr={"building":building, 'docstatus':1}
    fltr2={"building":building, 'docstatus':1}
    if hostel_room:
        fltr.update({"to_room":hostel_room})
        fltr2.update({"room":hostel_room})
    deallotment_list = [s.student for s in frappe.db.get_list("Hostel Deallotment",fltr2, 'student')]
    for st in frappe.get_all("Hostel Allotment",filters=fltr,fields=['student','student_name']):
        is_debarred=False
        for d in frappe.get_all("Disciplinary Complaints",{'student':st.student,'complaint_status':"Action Taken",'action':"Debarred","docstatus":1}):
            is_debarred=True
        if not is_debarred and st.student not in deallotment_list:
            student_list.append(st.update({"group_roll_number":count}))
            count+=1
    return student_list