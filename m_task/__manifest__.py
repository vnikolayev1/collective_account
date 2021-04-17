{
    'name': "M task",
    'summary': 'Stores product/buyer summary data in collective account table',

    'author': 'Vnikolayev',
    'website': 'https://github.com/vnikolayev1',

    'category': 'Sales/Sales',
    'license': 'OPL-1',
    'version': '14.0.0.0.1',
    'depends': [
        "base",
        "account",
        "sale_management",
        "contacts",
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/collective_account.xml',

    ],
    'external_dependencies': {
        'python': [],
    },
    'qweb': [],
    'demo': ['data/invoice_data.xml'],
    'auto_install': False,
    'installable': True,
    'application': True,
}
