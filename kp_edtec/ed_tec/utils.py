import frappe

def academic_term(doc):
	# parent field validation

	field_dict=get_field_dict_by_options(doc,["Academic Year","Academic Term"])
	if field_dict.get('Academic Year') and field_dict.get('Academic Term') and doc.get(field_dict.get('Academic Term')['fieldname']) and doc.get(field_dict.get('Academic Year')['fieldname']):
		if not frappe.db.get_value("Academic Term",{"name":doc.get(field_dict.get('Academic Term')['fieldname']),"academic_year":doc.get(field_dict.get('Academic Year')['fieldname'])}):
			frappe.throw("<b>{0}</b> Not Belongs to <b>{1}</b>".format(field_dict.get('Academic Term')['label'],field_dict.get('Academic Year')['label']))
	
	# child field validation

	child_field_dict=get_field_dict_by_options(doc,["Academic Year","Academic Term"],True)
	if not child_field_dict.get("Academic Year"):
		child_field_dict["Academic Year"]=field_dict.get("Academic Year")

	if child_field_dict.get('Academic Year') and child_field_dict.get('Academic Term'):
		for df in frappe.get_meta(doc.doctype).fields:
			if df.fieldtype =="Table":
				for child_doc in doc.get(df.fieldname):
					if child_doc.get(child_field_dict.get('Academic Term')['fieldname']) and (child_doc.get(child_field_dict.get('Academic Year')['fieldname']) or doc.get(child_field_dict.get('Academic Year')['fieldname'])):
						if not frappe.db.get_value("Academic Term",{"name":child_doc.get(child_field_dict.get('Academic Term')['fieldname']),"academic_year":(child_doc.get(child_field_dict.get('Academic Year')['fieldname']) or doc.get(child_field_dict.get('Academic Year')['fieldname']))}):
							frappe.throw("#Row {0} <b>{1}</b> Not Belongs to <b>{2}</b>".format(child_doc.idx,child_field_dict.get('Academic Term')['label'],child_field_dict.get('Academic Year')['label']))

def semester_belongs_to_programs(doc):
	# parent field validation

	field_dict=get_field_dict_by_options(doc,["Programs","Program"])
	if field_dict.get('Programs') and field_dict.get('Program') and doc.get(field_dict.get('Program')['fieldname']) and doc.get(field_dict.get('Programs')['fieldname']):
		if not frappe.db.get_value("Program",{"name":doc.get(field_dict.get('Program')['fieldname']),"programs":doc.get(field_dict.get('Programs')['fieldname'])}):
			frappe.throw("<b>{0}</b> Not Belongs to <b>{1}</b>".format(field_dict.get('Program')['label'],field_dict.get('Programs')['label']))
	
	# child field validation

	child_field_dict=get_field_dict_by_options(doc,["Programs","Program"],True)
	if not child_field_dict.get("Programs"):
		child_field_dict["Programs"]=field_dict.get("Programs")

	if child_field_dict.get('Programs') and child_field_dict.get('Program'):
		for df in frappe.get_meta(doc.doctype).fields:
			if df.fieldtype =="Table":
				for child_doc in doc.get(df.fieldname):
					if child_doc.get(child_field_dict.get('Program')['fieldname']) and (child_doc.get(child_field_dict.get('Programs')['fieldname']) or doc.get(child_field_dict.get('Programs')['fieldname'])):
						if not frappe.db.get_value("Program",{"name":child_doc.get(child_field_dict.get('Program')['fieldname']),"programs":(child_doc.get(child_field_dict.get('Programs')['fieldname']) or doc.get(child_field_dict.get('Programs')['fieldname']))}):
							frappe.throw("#Row {0} <b>{1}</b> Not Belongs to <b>{2}</b>".format(child_doc.idx,child_field_dict.get('Program')['label'],child_field_dict.get('Programs')['label']))

# def course_belongs_to_semester(doc):
# 	# parent field validation

# 	field_dict=get_field_dict_by_options(doc,["Program","Course"])
# 	if field_dict.get('Program') and field_dict.get('Course') and doc.get(field_dict.get('Course')['fieldname']) and doc.get(field_dict.get('Program')['fieldname']):
# 		if not frappe.db.get_value("Course",{"name":doc.get(field_dict.get('Course')['fieldname']),"programs":doc.get(field_dict.get('Program')['fieldname'])}):
# 			frappe.throw("<b>{0}</b> Not Belongs to <b>{1}</b>".format(field_dict.get('Course')['label'],field_dict.get('Program')['label']))
	
# 	# child field validation

# 	child_field_dict=get_field_dict_by_options(doc,["Program","Course"],True)
# 	if not child_field_dict.get("Program"):
# 		child_field_dict["Program"]=field_dict.get("Program")

# 	if child_field_dict.get('Program') and child_field_dict.get('Course'):
# 		for df in frappe.get_meta(doc.doctype).fields:
# 			if df.fieldtype =="Table":
# 				for child_doc in doc.get(df.fieldname):
# 					if child_doc.get(child_field_dict.get('Course')['fieldname']) and (child_doc.get(child_field_dict.get('Program')['fieldname']) or doc.get(child_field_dict.get('Program')['fieldname'])):
# 						if not frappe.db.get_value("Course",{"name":child_doc.get(child_field_dict.get('Course')['fieldname']),"programs":(child_doc.get(child_field_dict.get('Program')['fieldname']) or doc.get(child_field_dict.get('Program')['fieldname']))}):
# 							frappe.throw("#Row {0} <b>{1}</b> Not Belongs to <b>{2}</b>".format(child_doc.idx,child_field_dict.get('Course')['label'],child_field_dict.get('Program')['label']))
							

def get_field_dict_by_options(doc,options,is_child=False):
	field_dict={}
	if not is_child:
		for df in frappe.get_meta(doc.doctype).fields:
			for op in options:
				if op==df.options:
					field_dict[df.options]={"fieldname":df.fieldname,"label":df.label}
	else:
		for df in frappe.get_meta(doc.doctype).fields:
			if df.fieldtype =="Table":
				for child_df in frappe.get_meta(df.options).fields:
					for op in options:
						if op==child_df.options:
							field_dict[child_df.options]={"fieldname":child_df.fieldname,"label":child_df.label}
	return field_dict

def float_and_integer_fields(doc):		
	# parent field validation
	for df in frappe.get_meta(doc.doctype).fields: 
		if df.fieldtype in ["Int","Float"]:
			number_validation(doc,df)

		# child field validation
		elif df.fieldtype =="Table":
			for child_df in frappe.get_meta(df.options).fields: 
				if child_df.fieldtype in ["Int","Float"]:
					for child_doc in doc.get(df.fieldname):
						number_validation(child_doc,child_df,"#Row {0}".format(child_doc.idx))

def number_validation(doc,df,msg=""):
	if doc.get(df.fieldname) < 0:
		frappe.throw("{0} Field <b>{1}</b> value can not be negative".format(msg,df.label)) 
		
def date_greater_than(doc,from_date,to_date):
	field_dict={}
	for df in frappe.get_meta(doc.doctype).fields:
		field_dict[df.fieldname]=df
	
	if doc.get(from_date) and  doc.get(to_date) and doc.get(from_date) >= doc.get(to_date):
		frappe.throw("<b>{0}</b> Should be less than <b>{1}</b>".format(field_dict[from_date].label,field_dict[to_date].label))


def date_greater_than_or_equal(doc,from_date,to_date):
	field_dict={}
	for df in frappe.get_meta(doc.doctype).fields:
		field_dict[df.fieldname]=df
	
	if doc.get(from_date) and  doc.get(to_date) and doc.get(from_date) > doc.get(to_date):
		frappe.throw("<b>{0}</b> Should be less than or equal to <b>{1}</b>".format(field_dict[from_date].label,field_dict[to_date].label))


def duplicate_row_validation(doc,table_field_name,comapre_fields):
	row_names=[]
	for row in doc.get(table_field_name):
		row_names.append(row.name)

	for row in doc.get(table_field_name):
		filters={"parent":row.parent,"idx":("!=",row.idx)}
		for field in comapre_fields:
			filters[field]=row.get(field)
		for duplicate in frappe.get_all(row.doctype,filters,['idx','name']):
			if duplicate.name in row_names:
				frappe.throw("#Row {0} Duplicate values in <b>{1}</b> Not Allowed".format(duplicate.idx, table_field_name))


def get_courses_by_semester(semester):
	"""
	    semester:-"Sem1"
	OR  
		semester:-["Sem1","Sem2","Sem3"]
	"""
	course_list=[]
	filters={"parentfield": "courses","parenttype": "Program"}
	if type(semester)==str:
		filters.update({"parent":semester})
	elif type(semester)==dict:
		filters.update(semester)
	else:
		filters.update({"parent":["IN",semester]})

	for cr in frappe.get_all("Program Course",filters,['course']):
		if cr.course not in course_list:
			course_list.append(cr.course)
			
	return course_list