# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.depends('line_ids', 'line_ids.is_reconciled')
    def _compute_total_debit_credit(self):
        for b in self:
            debit = 0
            credit = 0

            for l in b.line_ids:
                if l.amount <= 0:
                    debit += l.amount
                if l.amount >= 0:
                    credit += l.amount

            b.credit_balance = credit
            b.debit_balance = debit


    debit_balance = fields.Monetary('Computed Debit', compute='_compute_total_debit_credit', store=True)
    credit_balance = fields.Monetary('Computed Credit', compute='_compute_total_debit_credit', store=True)
    date_start = fields.Date(string="Date Start", required=False)
