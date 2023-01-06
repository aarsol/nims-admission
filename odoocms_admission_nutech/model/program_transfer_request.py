import pdb

from odoo import fields, models, _, api


class ProgramTransferRequest(models.Model):
    _name = 'odoocms.program.transfer.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Program Transfer Request'
    _rec_name = 'applicant_id'

    applicant_id = fields.Many2one('odoocms.application', string='Application', required=True)
    current_program = fields.Many2one('odoocms.program', string='Requested Program')
    previous_program = fields.Many2one('odoocms.program', string='Current Program')
    prog_req = fields.Boolean(string='Program', default=False)
    pre_test_marks = fields.Integer(string='Pre Test Marks')
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('approve', 'Approve'), ('reject', 'Reject'), ],
        required=False, default='draft')

    def approve(self):
        self.prog_req = True
        for rec in self:
            rec.state = 'approve'
            program = self.env['odoocms.entry.schedule.details'].search(
                [('program_id', '=', rec.previous_program.id), ('status', '=', 'open')])
        if program.program_id[0]:
            program.write({
                'program_id': rec.current_program.id,
            })
        application_preference = self.env['odoocms.application'].search([('id', '=', rec.applicant_id.id)])
        for app in application_preference.preference_ids:
            if app.program_id[0]:
                app.write({
                    'program_id': rec.current_program.id,
                })
        application_preference.pre_test_marks = self.pre_test_marks
        applicant = self.env['applicant.entry.test'].search([('student_id', '=', rec.applicant_id.id)])
        applicant.entry_test_schedule_details_id.program_id = rec.current_program.id,

        merit_register = self.env['odoocms.merit.registers'].search([])
        for merit_register in merit_register.merit_register_ids:
            if merit_register.applicant_id.application_no == rec.applicant_id.application_no:
                merit_register.unlink()

        offer_letter = self.env['admission.offer.letter'].search([('applicant_id', '=', rec.applicant_id.id)])
        if offer_letter.applicant_id.application_no == rec.applicant_id.application_no:
            offer_letter.unlink()

        invoices = self.env['account.move'].search([('application_id', '=', rec.applicant_id.id),
                                                    ('payment_state', 'not in', ['in_payment', 'paid'])])

        # for rec in invoices:
        invoices.write({
            'posted_before': False,
            'payment_state': 'not_paid'
        })
        invoices.sudo().unlink()

        if rec.applicant_id.student_id:
            invoices = self.env['account.move'].search([('application_id', '=', rec.applicant_id.id),
                                                        ('payment_state', 'in', ['in_payment', 'paid'])])
            if invoices:
                # to check paid invoices
                amount = 0
                for im in invoices:
                    amount += im.amount_total
                rec.applicant_id.admission_create_student_ledger_entry(invoice=invoices[0], debit=amount, credit=0,
                                                                       description='OD')

    def reject(self):
        self.prog_req = True
        for rec in self:
            rec.state = 'reject'
