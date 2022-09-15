import frappe
import os


def validate(doc,method):
    file_size(doc)


def file_size(doc):
    file_name = doc.file_url.split('/')[-1]
    public_file_path = frappe.get_site_path('public', 'files', file_name)
    # private_file_path = frappe.get_site_path('private', 'files', file_name)
    # print("\n\n\n\n")
    # print(public_file_path)
    # print(private_file_path)
    # site="erp.soulunileaders.com"
    # url="/opt/bench/frappe-bench/sites/"+site+"/public"+doc.file_url
    url=public_file_path
    # print("\n\n\n\n\n")
    # print(url)
    ext=os.path.splitext(url)
    extstr=ext[1]
    ext_list=[".jpg",".jpeg",".jfif",".pjpeg",".pjp",".png"]
    for t in ext_list:
        if t==extstr:
            file_size = os.path.getsize(url)
            if (file_size > 200000):
                os.remove(url)
                return frappe.throw("Image Size cannot exceed 200KB. Please press the \"Clear\" button and upload an Image of smaller size.")