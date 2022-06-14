from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'student_group',
		'transactions': [
			{
				'label': _('Course Assessment'),
				'items': ['Course Assessment Result']
			},
			{
				'label': _('Course'),
				'items': ['Course Schedule']
			}
		]
	}