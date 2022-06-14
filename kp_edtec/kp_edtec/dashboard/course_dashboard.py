
from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'course',
		'transactions': [
			{
				'label': _('Program and Course'),
				'items': ['Program', 'Course Enrollment', 'Course Schedule']
			},
			{
				'label': _('Student'),
				'items': ['Student Group']
			},
			{
				'label': _('Course Assessment'),
				'items': ['Course Assessment Plan', 'Course Assessment Result']
			},
		]
	}