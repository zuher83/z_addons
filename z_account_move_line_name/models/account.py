# -*- coding: utf-8 -*-

import logging
from odoo import models, api, _

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'


    def _post(self, soft=True):
        res = super(AccountMove, self)._post(soft=True)
        for move in self:
            # if move.type in ('out_invoice','in_invoice','out_refund','in_refund'):
            if move.is_invoice(True):
                to_write = {
                    'line_ids': []
                }

                if not move.ref:
                    to_write['payment_reference'] = move._get_invoice_computed_reference()
                else:
                    to_write['payment_reference'] = move.ref


                date = move.invoice_date.strftime('%d/%m/%y')

                name = ('%s %s %s' % (move.name, date, move.partner_id.name[:35]))
                for line in move.line_ids.filtered(lambda line: line.account_id.user_type_id.type
                                                                in ('receivable', 'payable') or
                                                                line.account_id.user_type_id.internal_group in ('asset','liability')):
                    _logger.warning('--------%s' % line)
                    to_write['line_ids'].append((1, line.id, {'ref': to_write['payment_reference'], 'name': name}))
                move.write(to_write)

        return res


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def default_get(self, fields):
        rec = super(AccountPayment, self).default_get(fields)

        invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]

            date = ''
            if invoice['invoice_date']:
                date = invoice['invoice_date'].strftime('%d/%m/%y')

            rec['communication'] = (_('Pay %s %s %s') % (invoice['name'], date, invoice[
                                                                                    'commercial_partner_id'][1][:35]))

        return rec

    # def _prepare_payment_moves(self):
    #     result = super(account_payment, self)._prepare_payment_moves()
    #
    #     name = self.name
    #     if self.payment_type != 'transfer':
    #         name = ''
    #         if self.partner_type == 'customer':
    #             if self.payment_type == 'inbound':
    #                 name += _("Reg ")
    #             elif self.payment_type == 'outbound':
    #                 name += _("Rmb Clt.")
    #         elif self.partner_type == 'supplier':
    #             if self.payment_type == 'inbound':
    #                 name += _("Rmb Frns.")
    #             elif self.payment_type == 'outbound':
    #                 name += _("Reg Frns.")
    #
    #         if self.journal_id.id:
    #             name += self.journal_id.code + ' '
    #
    #         name += self.partner_id.name[:15] + ': '
    #
    #     for i in [x['line_ids'] for x in result]:
    #         # lines = [k['name'] for k,v in i['line_ids']]
    #         # lines = self.resolve_2many_commands(i['line_ids'], [])
    #         _logger.warn('Avant loop %s' % i)
    #
    #         for k in i[2].values():
    #             _logger.warn('Loop %s' % k)
    #
    #     # if invoice:
    #         #     for inv in invoice:
    #         #         name += inv.name
    #
    #     result.update({'name': name})
    #
    #     return result


#
#     def _get_counterpart_move_line_vals(self, invoice=False):
#         result = super(account_payment, self)._get_counterpart_move_line_vals(
#             invoice=invoice)
#
#         name = self.name
#         if self.payment_type != 'transfer':
#             name = ''
#             if self.partner_type == 'customer':
#                 if self.payment_type == 'inbound':
#                     name += _("Reg ")
#                 elif self.payment_type == 'outbound':
#                     name += _("Rmb Clt.")
#             elif self.partner_type == 'supplier':
#                 if self.payment_type == 'inbound':
#                     name += _("Rmb Frns.")
#                 elif self.payment_type == 'outbound':
#                     name += _("Reg Frns.")
#
#             if self.journal_id.id:
#                 name += self.journal_id.code + ' '
#
#             name += self.partner_id.name[:15] + ': '
#
#             if invoice:
#                 for inv in invoice:
#                     name += inv.number
#
#         result.update({'name': name})
#
#         return result
#
#     def _get_liquidity_move_line_vals(self, amount):
#         result = super(account_payment,
#                        self)._get_liquidity_move_line_vals(amount)
#         name = self.name
#
#         if self.payment_type != 'transfer':
#             name = ''
#             if self.partner_type == 'customer':
#                 if self.payment_type == 'inbound':
#                     name += _("Reg ")
#                 elif self.payment_type == 'outbound':
#                     name += _("Rmb Clt.")
#             elif self.partner_type == 'supplier':
#                 if self.payment_type == 'inbound':
#                     name += _("Rmb Frns.")
#                 elif self.payment_type == 'outbound':
#                     name += _("Reg Frns.")
#
#             if self.journal_id.id:
#                 name += self.journal_id.code + ' '
#
#             name += self.partner_id.name[:15] + ': '
#             if self.invoice_ids:
#                 for inv in self.invoice_ids:
#                     name += inv.number
#         result.update({'name': name})
#
#         return result
#
# class account_register_payments(models.TransientModel):
#     _inherit = 'account.register.payments'
#
#     @api.model
#     def default_get(self, fields):
#         rec = super(account_register_payments, self).default_get(fields)
#
#         context = dict(self._context or {})
#         active_model = context.get('active_model')
#         active_ids = context.get('active_ids')
#
#         invoices = self.env[active_model].browse(active_ids)
#         communication = ('%s %s %s' % (_('REG'), datetime.today().date(), invoices[0].commercial_partner_id.name[:49]))
#
#         rec.update({
#             'communication': communication,
#         })
#
#         return rec
