import time
from openerp.report import report_sxw
from openerp.osv import osv


class bankforwarding(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bankforwarding, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_detail_data_list': self.get_detail_data_list,
        })



    def get_detail_data_list(self, obj):

        department_wise_value=[]


        tmp_list=[]
        tmp_dict ={
            'employee_id':'',
            'employee_name':'',
            'designation':'',
            'acc_no':'',

        }
        tmp_dict['nes_sal'] = 0

        head_count=0
        for slip_items in obj.slip_ids:
            tmp_dict={}
            head_count=head_count+1
            tmp_dict['employee_id'] =slip_items.contract_id.employee_id.id
            tmp_dict['employee_name'] =slip_items.contract_id.employee_id.name
            tmp_dict['acc_no'] =slip_items.contract_id.employee_id.bank_account_id.acc_number
            tmp_dict['designation'] =slip_items.contract_id.employee_id.job_id.name

            pay_items =slip_items.line_ids
            tmp_dict['net_sal']=pay_items[19].total
            department_wise_value.append(tmp_dict)
        return department_wise_value





class report_batch_bank_forwarding(osv.AbstractModel):
    _name = 'report.payslip_report_batch.report_batch_bank_forwarding'
    _inherit = 'report.abstract_report'
    _template = 'payslip_report_batch.report_batch_bank_forwarding'
    _wrapped_report_class = bankforwarding