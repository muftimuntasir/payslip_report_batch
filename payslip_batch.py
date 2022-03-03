from datetime import datetime, timedelta
from openerp.osv import fields, osv
from openerp import api
from openerp.tools.translate import _



class PayslipBatchRun(osv.osv):
    _inherit = "hr.payslip.run"

    _columns = {
        'header_name': fields.char("Header Name")
    }



    def print_batch_payslip_report(self, cr, uid, ids, context=None):

        context = dict(context or {}, active_ids=ids)
        return self.pool.get("report").get_action(cr, uid, ids, 'payslip_report_batch.report_batch_payslip_layout', context=context)

    def print_bank_forwarding_report(self, cr, uid, ids, context=None):

        context = dict(context or {}, active_ids=ids)
        return self.pool.get("report").get_action(cr, uid, ids, 'payslip_report_batch.report_batch_bank_forwarding', context=context)

    def approve_payslive(self, cr, uid, ids, context=None):
        obj_self = self.browse(cr, uid, ids[0], context=context)
        # obj_self.slip_ids[0].details_by_salary_rule_category[10].total
        # basic=obj_self.slip_ids[2].details_by_salary_rule_category[0].amount
        # gross=obj_self.slip_ids[2].details_by_salary_rule_category[7].total
        # cpf=obj_self.slip_ids[2].details_by_salary_rule_category[10].total
        # cpfl=obj_self.slip_ids[2].details_by_salary_rule_category[12].total
        # group_in=obj_self.slip_ids[2].details_by_salary_rule_category[11].total
        # food=obj_self.slip_ids[2].details_by_salary_rule_category[14].total
        # sal_adv=obj_self.slip_ids[2].details_by_salary_rule_category[15].total
        # deduct_basic=obj_self.slip_ids[2].details_by_salary_rule_category[16].total
        # stamp=obj_self.slip_ids[2].details_by_salary_rule_category[17].total
        # NET=obj_self.slip_ids[2].details_by_salary_rule_category[19].total

        total_gross=0
        total_group_ins=0
        company_contibution_cpf=0
        total_stamp=0
        total_net=0
        company_g_ins=0
        total_salary_payable=0
        food_payable=0
        basic_deduct=0

        jv_entry = self.pool.get('account.move')

        if context is None: context = {}
        if context.get('period_id', False):
            return context.get('period_id')
        periods = self.pool.get('account.period').find(cr, uid, context=context)
        period_id = periods and periods[0] or False
        line_ids = []
        for payslip in obj_self.slip_ids:
            total_gross = total_gross + payslip.details_by_salary_rule_category[7].total
            total_net = total_net + payslip.details_by_salary_rule_category[19].total
            total_stamp = total_stamp + payslip.details_by_salary_rule_category[17].total
            company_contibution_cpf = company_contibution_cpf + payslip.details_by_salary_rule_category[8].total
            company_g_ins = company_g_ins + payslip.details_by_salary_rule_category[9].total
            g_ins_emp=payslip.details_by_salary_rule_category[11].total
            cpf_emp=payslip.details_by_salary_rule_category[10].total
            cpf_loan=payslip.details_by_salary_rule_category[12].total
            emp_sal_adv=payslip.details_by_salary_rule_category[15].total
            emp_income_tax=payslip.details_by_salary_rule_category[13].total
            food_payable=food_payable+payslip.details_by_salary_rule_category[14].total
            basic_deduct=basic_deduct+payslip.details_by_salary_rule_category[16].total
            # import pdb
            # pdb.set_trace()

            contract_id=payslip.contract_id
            pf_account_id=contract_id.pf_account_id.id
            loan_account_id=contract_id.loan_account_id.id


            if cpf_emp>0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': obj_self.name,
                    'currency_id': False,
                    'credit': cpf_emp,
                    'date_maturity': False,
                    'account_id': pf_account_id,
                    ### Accounts Receivable ID
                    'debit': 0,
                    'amount_currency': 0,
                    'partner_id': False,
                }))
            if g_ins_emp>0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': obj_self.name,
                    'currency_id': False,
                    'credit': g_ins_emp,
                    'date_maturity': False,
                    'account_id': 7254,
                    ### Accounts Receivable ID
                    'debit': 0,
                    'amount_currency': 0,
                    'partner_id': False,
                }))
            if cpf_loan>0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': obj_self.name,
                    'currency_id': False,
                    'credit': cpf_loan,
                    'date_maturity': False,
                    'account_id': loan_account_id,
                    ### Accounts Receivable ID
                    'debit': 0,
                    'amount_currency': 0,
                    'partner_id': False,
                }))
            if emp_sal_adv>0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': contract_id.name,
                    'currency_id': False,
                    'credit': emp_sal_adv,
                    'date_maturity': False,
                    'account_id': 303,
                    ### Accounts Receivable ID
                    'debit': 0,
                    'amount_currency': 0,
                    'partner_id': False,
                }))
            if emp_income_tax>0:
                line_ids.append((0, 0, {
                    'analytic_account_id': False,
                    'tax_code_id': False,
                    'tax_amount': 0,
                    'name': obj_self.name,
                    'currency_id': False,
                    'credit': emp_income_tax,
                    'date_maturity': False,
                    'account_id': 7256,
                    ### Accounts Receivable ID
                    'debit': 0,
                    'amount_currency': 0,
                    'partner_id': False,
                }))

        total_salary_payable = total_gross +company_g_ins + company_contibution_cpf
        #this line_ids for total salary expense
        line_ids.append((0, 0, {
            'analytic_account_id': False,
            'tax_code_id': False,
            'tax_amount': 0,
            'name': obj_self.name,
            'currency_id': False,
            'credit': 0,
            'date_maturity': False,
            'account_id': 7255,
            ### Accounts Receivable ID
            'debit': total_salary_payable,
            'amount_currency': 0,
            'partner_id': False,
        }))
        # this line_ids for total net salary
        line_ids.append((0, 0, {
            'analytic_account_id': False,
            'tax_code_id': False,
            'tax_amount': 0,
            'name': obj_self.name,
            'currency_id': False,
            'credit': total_net,
            'date_maturity': False,
            'account_id': 7258,
            ### Accounts Receivable ID
            'debit': 0,
            'amount_currency': 0,
            'partner_id': False,
        }))
        if total_stamp > 0:
            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': obj_self.name,
                'currency_id': False,
                'credit': total_stamp,
                'date_maturity': False,
                'account_id': 7257,
                ### Accounts Receivable ID
                'debit': 0,
                'amount_currency': 0,
                'partner_id': False,
            }))

        if food_payable > 0:
            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': obj_self.name,
                'currency_id': False,
                'credit': food_payable,
                'date_maturity': False,
                'account_id': 7259,
                ### Accounts Receivable ID
                'debit': 0,
                'amount_currency': 0,
                'partner_id': False,
            }))
        if basic_deduct > 0:
            line_ids.append((0, 0, {
                'analytic_account_id': False,
                'tax_code_id': False,
                'tax_amount': 0,
                'name': "basic deduct",
                'currency_id': False,
                'credit': basic_deduct,
                'date_maturity': False,
                'account_id': 7260,
                ### Accounts Receivable ID
                'debit': 0,
                'amount_currency': 0,
                'partner_id': False,
            }))

        debit=0
        credit=0
        for item in line_ids:
            debit=debit+item[2]['debit']
            credit=credit+item[2]['credit']

        if debit!=credit:
            if debit>credit:
                differnece_amount=debit-credit
                if differnece_amount > 0:
                    line_ids.append((0, 0, {
                        'analytic_account_id': False,
                        'tax_code_id': False,
                        'tax_amount': 0,
                        'name': "basic deduct",
                        'currency_id': False,
                        'credit': differnece_amount,
                        'date_maturity': False,
                        'account_id': 7261,
                        ### Accounts Receivable ID
                        'debit': 0,
                        'amount_currency': 0,
                        'partner_id': False,
                    }))
            elif debit<credit:
                differnece_amount=credit-debit
                if differnece_amount > 0:
                    line_ids.append((0, 0, {
                        'analytic_account_id': False,
                        'tax_code_id': False,
                        'tax_amount': 0,
                        'name': "basic deduct",
                        'currency_id': False,
                        'credit': 0,
                        'date_maturity': False,
                        'account_id': 7261,
                        ### Accounts Receivable ID
                        'debit': differnece_amount,
                        'amount_currency': 0,
                        'partner_id': False,
                    }))

        #code for journal entries


        j_vals = {'name': '/',
                  'journal_id': 2,  ## Sales Journal
                  'date': fields.date.today(),
                  'period_id': period_id,
                  'ref': obj_self.name,
                  'line_id': line_ids

                  }

        saved_jv_id = jv_entry.create(cr, uid, j_vals, context=context)
        if saved_jv_id > 0:
            if saved_jv_id > 0:
                journal_id = saved_jv_id
                try:
                    jv_entry.button_validate(cr,uid, [saved_jv_id], context)
                except:
                    import pdb
                    pdb.set_trace()
        #end journal

        return True

    def disburse_payslip(self, cr, uid, ids, context=None):
        if not ids: return []
        inv = self.browse(cr, uid, ids[0], context=context)
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'payslip_report_batch','disburse_batch_form_view')
        #

        # total=inv.total
        # import pdb
        # pdb.set_trace()
        return {
            'name': _("Pay Invoice"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'disburse.batch',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_batch_id': ids[0]
            }
        }
        raise osv.except_osv(_('Error!'), _('There is no default company for the current user!'))




