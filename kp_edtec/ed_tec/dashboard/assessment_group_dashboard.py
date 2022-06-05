
from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'assessment_group',
		'transactions': [
			{
				'label': _('Course Assessment'),
				'items': ['Course Assessment Plan', 'Course Assessment Result']
			},
		]
	}