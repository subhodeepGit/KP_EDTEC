import frappe

def validate(self, method):
    if self.party_type=="Student":
        student_info=frappe.db.get_list("Student",filters={"name":self.party},fields=["roll_no"])
        self.roll_no=student_info[0]["roll_no"]
       

    self.letter_head=""

