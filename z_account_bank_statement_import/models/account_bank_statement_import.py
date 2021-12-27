# -*- coding: utf-8 -*-

from odoo import fields, models, _

class AccountStatementImport(models.TransientModel):
    _inherit = 'account.statement.import'

    statement_id = fields.Many2one(string='Statement', help='Choose existing statement',
                                   comodel_name='account.bank.statement', domain=[('state', '!=', 'confirm')], )

    def _create_bank_statements(self, stmts_vals, result):
        """Create new bank statements from imported values,
        filtering out already imported transactions,
        and return data used by the reconciliation widget"""
        abs_obj = self.env["account.bank.statement"]
        absl_obj = self.env["account.bank.statement.line"]

        # Filter out already imported transactions and create statements
        statement_ids = []
        existing_st_line_ids = {}
        for st_vals in stmts_vals:
            st_lines_to_create = []
            for lvals in st_vals["transactions"]:
                existing_line = False
                if lvals.get("unique_import_id"):
                    existing_line = absl_obj.sudo().search(
                        [
                            ("unique_import_id", "=",
                             lvals["unique_import_id"]),
                        ],
                        limit=1,
                    )
                    # we can only have 1 anyhow because we have a unicity SQL constraint
                if existing_line:
                    existing_st_line_ids[existing_line.id] = True
                    if "balance_start" in st_vals:
                        st_vals["balance_start"] += float(lvals["amount"])
                else:
                    st_lines_to_create.append(lvals)

            if len(st_lines_to_create) > 0:
                if not st_lines_to_create[0].get("sequence"):
                    for seq, vals in enumerate(st_lines_to_create, start=1):
                        vals["sequence"] = seq
                # Remove values that won't be used to create records
                st_vals.pop("transactions", None)
                # Create the statement with lines
                st_vals["line_ids"] = [[0, False, line]
                                       for line in st_lines_to_create]

                if self.statement_id:
                    st_vals['name'] = self.statement_id.name
                    statement_ids.append(abs_obj.with_context(
                        check_move_validity=False).browse(self.statement_id.id).write(st_vals))
                    statement_ids.remove(True)
                    statement_ids.append(self.statement_id.id)
                elif not self.statement_id:
                    statement = abs_obj.create(st_vals)
                    statement_ids.append(statement.id)

        if not statement_ids:
            return False
        result["statement_ids"].extend(statement_ids)

        # Post lines if statement state is 'posted'
        if self.statement_id.state == 'posted':
            lines_of_moves_to_post = self.statement_id.line_ids.filtered(
                lambda line: line.move_id.state != 'posted')
            if lines_of_moves_to_post:
                lines_of_moves_to_post.move_id._post(soft=False)

        # Prepare import feedback
        num_ignored = len(existing_st_line_ids)
        if num_ignored > 0:
            result["notifications"].append(
                {
                    "type": "warning",
                    "message": _(
                        "%d transactions had already been imported and were ignored."
                    )
                    % num_ignored
                    if num_ignored > 1
                    else _("1 transaction had already been imported and was ignored."),
                    "details": {
                        "name": _("Already imported items"),
                        "model": "account.bank.statement.line",
                        "ids": list(existing_st_line_ids.keys()),
                    },
                }
            )
