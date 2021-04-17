import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class CollectiveAccount(models.Model):
    _name = 'collective.account'

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product name')
    total_product_qty = fields.Float()
    total_product_price = fields.Float()
    partner_id = fields.Many2one(comodel_name='res.partner')
