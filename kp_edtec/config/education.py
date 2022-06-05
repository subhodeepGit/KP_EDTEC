from __future__ import unicode_literals
from frappe import _

def get_data():
	
	return [
		{
			"label": _("Exam"),
			"items": [
				{
					"type": "doctype",
					"name": "Exam Application",
				},
				{
					"type": "doctype",
					"name": "Exam Declaration"
				},
				{
					"type": "doctype",
					"name": "Exam Paper Setting"
				},
				{
					"type": "doctype",
					"name": "Exam Application Courses"
				}
			]
		},
	]
	
