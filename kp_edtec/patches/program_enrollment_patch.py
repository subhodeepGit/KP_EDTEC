import frappe
# bench execute kp_edtec.patches.program_enrollment_patch.set_course_name
def execute():
    set_course_name()
    
def set_course_name():
    for enroll in frappe.get_all("Program Enrollment",{"docstatus":0}):
        print(enroll)
        doc=frappe.get_doc("Program Enrollment",enroll.name)
        semester=frappe.get_doc("Program",doc.program)
        courses=[d.course for d in semester.get("courses")]

        duplicate_courses=[]
        for cr in doc.get("courses"):
            if cr.course not in duplicate_courses:
                duplicate_courses.append(cr.course)

        doc.set("courses",[])
        for cr in duplicate_courses:
            for course in frappe.get_all("Course",{"name":cr},["course_name","course_code","mode"]):
                if cr not in courses:
                    courses.append(cr)
                    semester=frappe.get_doc("Program",doc.program)
                    semester.append("courses",{
                        "course":cr,
                        "course_name":course.course_name,
                        "modes":course.mode
                    })
                    semester.save()

                doc.append("courses",{
                            "course":cr,
                            "course_name":course.course_name,
                            "course_code":course.course_code
                        })
    
        doc.save()  
        doc.submit()          
