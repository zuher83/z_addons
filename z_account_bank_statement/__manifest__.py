# -*- coding: utf-8 -*-

{
    'name': 'Z Account Bank Statement',
    'version': '1',
    'description': """
This module add in footer new field (debit / credit) in bank statement views and change lines color if debit/credit.

    """,
    'author': 'Zuher Elmas',
    'category': 'Z Modules Account',
    'depends': ['account'],
    'data': ['views/account_bank_statement.xml'],
    'installable': True,
    'application': False,

}
