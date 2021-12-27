# -*- coding: utf-8 -*-
{
    'name': 'Import In Existing Bank Statement',
    'version': '1',
    'license': 'AGPL-3',
    'category': 'Z Modules',
    'description': """
Import In Existing Bank Statement
=================================
* Allow to import new records in existing statement
    """,
    'author': 'Zuher ELMAS',
    'depends': ['account_statement_import'],
    'data': [
            'views/account_bank_statement_import_view.xml',
             # 'security/------.xml',
            ],
    'installable': True,
}
