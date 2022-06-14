from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'room',
		'transactions': [
			{
				'label': _('Course'),
				'items': ['Course Schedule']
			},
			{
				'label': _('Course Assessment'),
				'items': ['Course Assessment Plan']
			}
		]
	}