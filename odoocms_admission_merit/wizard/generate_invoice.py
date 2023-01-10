import pdb
from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


class GenerateInvoice(models.Model):
    _name = 'generate.invoice'
    _description = 'Generate Invoice'
    _rec_name = 'merit_id'

    merit_id = fields.Many2one('odoocms.merit.registers', string='Merit', required=True)
    program_id = fields.Many2one('odoocms.program', string='Program', required=True)

    @api.onchange('merit_id')
    def onchange_merit_id(self):
        for rec in self:
            return {'domain': {'program_id': [('id', 'in', rec.merit_id.program_ids.program_id.ids)]}}

    def generate_admission_invoices(self):
        invoice_list = self.env['invoice.list'].search([])
        invoice_list.unlink()
        for merit_line in self.merit_id.merit_register_ids.filtered(lambda x: x.selected==True):
            check_application = merit_line.applicant_id
            if check_application.fee_voucher_state=='verify' and check_application.applicant_academic_ids.filtered(lambda x: x.doc_state=='yes'):
                list = self.env['invoice.list'].sudo()
                list.create({
                    'applicant_id': check_application.id,
                    'document_state': 'Verified',
                })
                check_application.action_create_admission_invoice()

            elif check_application.fee_voucher_state!='verify' or check_application.applicant_academic_ids.filtered(lambda x: x.doc_state!='yes'):
                list = self.env['invoice.list'].search([])
                list.create({
                    'applicant_id': check_application.id,
                    'document_state': 'Not Verified',
                })
