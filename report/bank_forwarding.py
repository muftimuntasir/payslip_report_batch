import time
from openerp.report import report_sxw
from openerp.osv import osv


class batchbankforwarding(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(batchbankforwarding, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_detail_data_list': self.get_detail_data_list,
        })



    def get_detail_data_list(self, obj):

        department_wise_value=[]


        tmp_list=[]
        tmp_dict ={
            'employee_id':'',
            'employee_name':'',
            'joining_date':'',
            'department_name':'',
            'designation':'',
            'gross_salary':0,
            'total_addition':0,
            'total_deduction':0,
            'net_apyable':0,
            'ac_no':'',

        }
        tmp_dict['basic'] = 0
        tmp_dict['house_rent'] = 0
        tmp_dict['medical'] = 0
        tmp_dict['arrear'] =0
        tmp_dict['dear_allow'] =0
        tmp_dict['other_allow'] = 0
        tmp_dict['total_allow'] = 0
        tmp_dict['gross'] = 0
        tmp_dict['p_fund'] = 0
        tmp_dict['g_ins'] = 0
        tmp_dict['cpf'] = 0
        tmp_dict['group_ins'] = 0
        tmp_dict['cpf_loan'] = 0
        tmp_dict['income_tax'] = 0
        tmp_dict['food'] = 0
        tmp_dict['adv_sal'] = 0
        tmp_dict['basic_deduct'] = 0
        tmp_dict['stamp'] = 0
        tmp_dict['total_deduct'] = 0
        tmp_dict['nes_sal'] = 0

        head_count=0
        for slip_items in obj.slip_ids:
            tmp_dict={}
            head_count=head_count+1
            tmp_dict['employee_id'] =slip_items.contract_id.employee_id.id
            tmp_dict['employee_name'] =slip_items.contract_id.employee_id.name
            tmp_dict['joining_date'] =slip_items.contract_id.date_start

            tmp_dict['department_name'] =slip_items.contract_id.employee_id.department_id.name
            tmp_dict['designation'] =slip_items.contract_id.employee_id.job_id.name
            tmp_dict['ac_no'] =''



            pay_items =slip_items.line_ids
            tmp_dict['basic']=pay_items[0].total
            tmp_dict['house_rent']=pay_items[1].total
            tmp_dict['medical']=pay_items[2].total
            tmp_dict['arrear']=pay_items[3].total
            tmp_dict['dear_allow']=pay_items[4].total
            tmp_dict['other_allow']=pay_items[5].total
            tmp_dict['total_allow']=pay_items[6].total
            tmp_dict['gross']=pay_items[7].total
            tmp_dict['p_fund']=pay_items[8].total
            tmp_dict['g_ins']=pay_items[9].total
            tmp_dict['cpf']=pay_items[10].total
            tmp_dict['group_ins']=pay_items[11].total
            tmp_dict['cpf_loan']=pay_items[12].total
            tmp_dict['income_tax']=pay_items[13].total
            tmp_dict['food']=pay_items[14].total
            tmp_dict['adv_sal']=pay_items[15].total
            tmp_dict['basic_deduct']=pay_items[16].total
            tmp_dict['stamp']=pay_items[17].total
            tmp_dict['total_deduct']=pay_items[18].total
            tmp_dict['net_sal']=pay_items[19].total



            department_wise_value.append(tmp_dict)





        return department_wise_value





class report_batch_payslip_layout(osv.AbstractModel):
    _name = 'report.payslip_report_batch.report_batch_payslip_layout'
    _inherit = 'report.abstract_report'
    _template = 'payslip_report_batch.report_batch_payslip_layout'
    _wrapped_report_class = batchbankforwarding