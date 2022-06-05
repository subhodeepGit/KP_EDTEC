from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'hostel_admission',
		'transactions': [
			{
				'label': _('Fee'),
				'items': ['Fees']
			},
		]
	}