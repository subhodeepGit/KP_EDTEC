from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'grading_scale',
		'non_standard_fieldnames': {
			'Course': 'default_grading_scale'
		},
		'transactions': [
			{
				'label': _('Course'),
				'items': ['Course']
			},
			{
				'label': _('Course Assessment'),
				'items': ['Course Assessment Plan', 'Course Assessment Result']
			}
		]
	}
