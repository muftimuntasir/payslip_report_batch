from openerp.osv import osv, fields
from openerp import SUPERUSER_ID, api
from openerp.tools.translate import _
from datetime import datetime




class disburse_batch(osv.osv):
    _name = 'disburse.batch'
    _description = "Disburse Batch"


    def button_confirm(self,cr,uid,ids,context=None):
        obj_self=self.browse(cr, uid, ids,context)
        batch_id=obj_self.batch_id
        batch_ids=batch_id.id

        bank_cash_account=obj_self.bank_cash_id.id
        total_net=0
        for payslip in batch_id.slip_ids:
            total_net = total_net + payslip.details_by_salary_rule_category[19].total


        # ###journal_entry
        journal_object = self.pool.get("bill.journal.relation")
        line_ids = []

        if context is None: context = {}
        if context.get('period_id', False):
            return context.get('period_id')
        periods = self.pool.get('account.period').find(cr, uid, context=context)
        period_id = periods and periods[0] or False
        # if payment method is cash
        # import pdb
        # pdb.set_trace()

        if total_net>0:

            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': batch_id.name,
                'currency_id': False,
                'credit': 0,
                'date_maturity': False,
                'account_id': 7258,  ### net salary payable account
                'debit': total_net,
                'amount_currency': 0,
                'partner_id': False,
            }))
            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': batch_id.name,
                'currency_id': False,
                'credit': total_net,
                'date_maturity': False,
                'account_id': bank_cash_account,  ### Cash ID
                'debit': 0,
                'amount_currency': 0,
                'partner_id': False,
            }))



        jv_entry = self.pool.get('account.move')

        j_vals = {'name': '/',
                  'journal_id': 2,  ## Cash Journal
                  'date': fields.date.today(),
                  'period_id': period_id,
                  'ref': batch_id.name,
                  'line_id': line_ids
                  }

        # import pdb
        # pdb.set_trace()
        saved_jv_id = jv_entry.create(cr, uid, j_vals, context=context)

        if saved_jv_id > 0:
            if saved_jv_id > 0:
                journal_id = saved_jv_id
                try:
                    jv_entry.button_validate(cr,uid, [saved_jv_id], context)
                    # cr.execute("update hr_payslip_run set state='close' where id=%s", (batch_ids))
                    # cr.commit()

                except:
                    import pdb
                    pdb.set_trace()
        ###end journal

        return saved_jv_id


    _columns = {
        'name':fields.char("Name"),
        'bank_cash_id':fields.many2one("account.account","Bank/Cash Account"),
        'batch_id': fields.many2one('hr.payslip.run', 'Payslip ID')
    }

    def create(self,cr,uid,vals,context):
        storedpayment = super(disburse_batch, self).create(cr, uid, vals, context)  # return ID int object
        return storedpayment
