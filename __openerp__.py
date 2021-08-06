{
    'name': 'Batch Payslip Report With Top Chart',
    'version': '8.0.0',
    'category': 'Sales',
    'description': """
Packing all invoices and delivery challans are printed from individual button action.  
=====================================================================================

""",
    'author': 'Mufti Muntasir Ahmed',
    'depends': [
        'hr',
        'hr_contract',
        'hr_holidays',
        'decimal_precision',
        'report',
    ],
    'data': [
        'views/report_batch_payslip_layout.xml',


        'batch_payslip_menu.xml',

        'batch_inherit_view.xml',

    ],

    'installable': True,
    'auto_install': False,
}