import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for obj in self:
            for invoice_line_id in obj.invoice_line_ids:
                if invoice_line_id.product_id.type != 'consu':
                    continue
                line_prod_id = invoice_line_id.product_id.id if \
                    invoice_line_id.product_id else False
                line_partner_id = obj.partner_id.id if \
                    obj.partner_id else False
                collective_record_id = self.env['collective.account'].search([
                    ('product_id', '=', line_prod_id),
                    ('partner_id', '=', line_partner_id)
                ], limit=1)
                if collective_record_id:
                    collective_record_id.total_product_qty += \
                        invoice_line_id.quantity
                    collective_record_id.total_product_price += \
                        invoice_line_id.price_subtotal
                else:
                    self.env['collective.account'].create({
                        'partner_id': line_partner_id,
                        'product_id': line_prod_id,
                        'total_product_qty': invoice_line_id.quantity,
                        'total_product_price': invoice_line_id.price_subtotal,
                    })
        return res
