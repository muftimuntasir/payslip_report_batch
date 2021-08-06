from datetime import datetime, timedelta
from openerp.osv import fields, osv
from openerp import api



class PayslipBatchRun(osv.osv):
    _inherit = "hr.payslip.run"



    def print_batch_payslip_report(self, cr, uid, ids, context=None):

        context = dict(context or {}, active_ids=ids)
        return self.pool.get("report").get_action(cr, uid, ids, 'payslip_report_batch.report_batch_payslip_layout', context=context)




