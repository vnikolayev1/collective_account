from odoo.tests.common import SavepointCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestAccountMoveCollective(SavepointCase):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super(TestAccountMoveCollective, cls).setUpClass()

        cls.partner_1 = cls.env.ref('base.res_partner_address_15')
        cls.partner_2 = cls.env.ref('base.res_partner_address_16')

        cls.product_1 = cls.env.ref('m_task.m_task_product_1')
        cls.product_2 = cls.env.ref('m_task.m_task_product_2')
        cls.product_3 = cls.env.ref('m_task.m_task_product_3')
        cls.collective_account_ids = cls.env['collective.account'].search([])
        AccountMove = cls.env['account.move'].with_context(
            tracking_disable=True)
        #invoices
        #partner 1 product 1 consumable
        cls.invoice_1 = AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner_1.id,
            'invoice_line_ids': [
                (0, 0, {'product_id': cls.product_1.id,
                        'price_unit': 10.0,
                        'quantity': 1}),
            ]
        })
        cls.invoice_2 = AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner_1.id,
            'invoice_line_ids': [
                (0, 0, {'product_id': cls.product_1.id,
                        'price_unit': 10.0,
                        'quantity': 2}),
            ]
        })
        #partner2 product1 consumable
        cls.invoice_3 = AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner_2.id,
            'invoice_line_ids': [
                (0, 0, {'product_id': cls.product_1.id,
                        'price_unit': 10.0,
                        'quantity': 4}),
            ]
        })
        #partner2 product2 consumable
        cls.invoice_4 = AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner_2.id,
            'invoice_line_ids': [
                (0, 0, {'product_id': cls.product_2.id,
                        'price_unit': 10.0,
                        'quantity': 5}),
            ]
        })
        #partner2 product1 and product2 service
        cls.invoice_5 = AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner_2.id,
            'invoice_line_ids': [
                (0, 0, {'product_id': cls.product_1.id,
                        'price_unit': 10.0,
                        'quantity': 4}),
                (0, 0, {'product_id': cls.product_3.id,
                        'price_unit': 15.0,
                        'quantity': 2}),
            ]
        })

    def test_invoice_confirm_to_collective_logic(self):
        #create first entry in collective
        self.invoice_1.action_post()
        created_col_ids = self.env['collective.account'].search([
            ('partner_id', '=', self.partner_1.id),
            ('product_id', '=', self.product_1.id),
        ])
        self.assertEqual(
            len(self.collective_account_ids) + len(created_col_ids),
            len(self.collective_account_ids) + 1)
        self.assertEqual(created_col_ids[0].total_product_price, 10.0)
        self.assertEqual(created_col_ids[0].total_product_qty, 1)
        # add value to first entry in collective
        self.invoice_2.action_post()
        added_col_ids = self.env['collective.account'].search([
            ('partner_id', '=', self.partner_1.id),
            ('product_id', '=', self.product_1.id),
        ])
        self.assertEqual(
            len(self.collective_account_ids) + len(added_col_ids),
            len(self.collective_account_ids) + 1)
        self.assertEqual(added_col_ids[0].total_product_price, 30.0)
        self.assertEqual(added_col_ids[0].total_product_qty, 3)
        # create second entry in collective
        self.invoice_3.action_post()
        created_col_ids = self.env['collective.account'].search([
            ('partner_id', '=', self.partner_2.id),
            ('product_id', '=', self.product_1.id),
        ])
        self.assertEqual(
            len(self.collective_account_ids) + len(created_col_ids) + 1,
            len(self.collective_account_ids) + 2)
        self.assertEqual(created_col_ids[0].total_product_price, 40.0)
        self.assertEqual(created_col_ids[0].total_product_qty, 4)
        # ignore creating entries when product is not consumable
        self.invoice_4.action_post()
        existing_col_ids = self.env['collective.account'].search([
            ('partner_id', '=', self.partner_2.id),
            ('product_id', '=', self.product_1.id),
        ])
        self.assertEqual(
            len(self.collective_account_ids) + len(existing_col_ids) + 1,
            len(self.collective_account_ids) + 2)
        # add value to few entries from one invoice
        self.invoice_5.action_post()
        product1_col_ids = self.env['collective.account'].search([
            ('partner_id', '=', self.partner_2.id),
            ('product_id', '=', self.product_1.id),
        ])
        product3_col_ids = self.env['collective.account'].search([
            ('partner_id', '=', self.partner_2.id),
            ('product_id', '=', self.product_3.id),
        ])
        self.assertEqual(
            len(self.collective_account_ids) + len(product1_col_ids) + len(
                product3_col_ids) + 1,
            len(self.collective_account_ids) + 3)
        self.assertEqual(product1_col_ids[0].total_product_price, 80.0)
        self.assertEqual(product1_col_ids[0].total_product_qty, 8)
        self.assertEqual(product3_col_ids[0].total_product_price, 30.0)
        self.assertEqual(product3_col_ids[0].total_product_qty, 2)
