import frappe,requests,json

def execute():
	response = requests.get("http://country.io/phone.json")
	if response.status_code == 200:
		if type(response._content)==bytes:
			data=json.loads(response._content.decode('utf-8'))
		else:
			data=json.loads(response._content)

		for cnt in frappe.get_all("Country"):
			country=frappe.get_doc("Country",cnt.name)
			country.country_phone_code=("+"+data.get((country.code).upper()))
			country.save()
