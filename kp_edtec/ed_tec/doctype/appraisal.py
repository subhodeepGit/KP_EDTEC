import frappe
import yaml

@frappe.whitelist()
def execute():
    with open("/home/tushar/Downloads/SQLDBM_DDL_input.txt") as sql:
        sql=sql.read()
        sql=sql.replace("(","$",1)
        sql=sql[::-1].replace(")","$",1)
        sql=sql[::-1]
        field_string=sql.split("$")[1]
        field_list=[]
        for f in field_string.split(","):

            field_dict={}
            field_dict['name']=(f.split()[0]).replace('"','')
            if len(f.split("COMMENT"))>1:
                field_dict['description']=(f.split("COMMENT")[1]).replace("'","")
            field_list.append(field_dict)

        data={}
        data['columns']=field_list
        table_name=sql.split("CREATE TABLE")[1]
        table_name=table_name.split("$")[0]
        data['name']=((table_name.rstrip("\n")).replace('"',""))
        description=sql.split("$")[-1]
        data['description']=description.split("'")[1]
        with open("outfile.yaml", 'w') as yfile:
            yaml.dump({"versions":2,"models":data}, yfile)
