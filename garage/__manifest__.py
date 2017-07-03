# -*- coding: utf-8 -*-
{
    'name': 'Garage',
    'version': '1.0',
    'category': 'Automobiles',
    'Author': 'Pankaj K',
    'Mail': 'kamanipankaj9099@gmail.com',
    'description': """
    * Alighnment Garage management
    * Expense
    * Accounting
    """,
    'depends': ['base', 'hr', 'report'],
    'data': [
        'security/garage_groups.xml',
        'security/ir.model.access.csv',
        'views/sequence.xml',
        'views/garage_views.xml',
        'views/service_charge_view.xml',
        'views/templates.xml',
        'views/garage_reports.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
