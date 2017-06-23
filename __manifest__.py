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
    'depends': ['base', 'hr'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/sequence.xml',
        'views/garage_views.xml',
        'views/service_charge_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
