from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on the Time Sheets created against this project'),
		'fieldname': 'user',
        'non_standard_fieldnames': {
            'ToDo':'owner'
        },
		'transactions': [
			{
				'label': _('Profile'),
				'items': ['Contact', 'Chat Profile', 'Blogger']
			},
			{
				'label': _('Logs'),
				'items': ['Access Log', 'Activity Log','Energy Point Log', 'Route History']
			},
			{
				'label': _('Settings'),
				'items': ['User Permission', 'Document Follow']
			},
			{
				'label': _('Activity'),
				'items': ['Communication', 'ToDo']
			},
		]
	}
