import pdb

from odoo import fields, models, _, api
from datetime import date
import random
import string
from odoo.exceptions import ValidationError


class ApplicantEntryTest(models.Model):
    _name = 'applicant.entry.test'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Applicant Entry Test'
    _rec_name = 'student_id'

    entry_test_schedule_details_id = fields.Many2one('odoocms.entry.schedule.details', string='Program')
    student_id = fields.Many2one('odoocms.application', string='Application')
    applicant = fields.Char(related='student_id.name', string='Applicant')
    reference_no = fields.Char(related='student_id.application_no', string='Reference no')
    room = fields.Many2one(string='Room',
                           related='entry_test_schedule_details_id.entry_schedule_id.entry_test_room_id', store=True)
    slots = fields.Many2one(string='Slots',
                            related='entry_test_schedule_details_id.entry_schedule_id.entry_test_slots_id', store=True)
    date = fields.Date(string='Date',
                       related='entry_test_schedule_details_id.entry_schedule_id.date', store=True)
    entry_test_marks = fields.Float('CBT Total Marks', compute='_entry_test_marks', store=True)
    cbt_marks = fields.Float('CBT Marks')
    cbt_id = fields.Integer(string='CBT ID')
    master_id = fields.Integer(string='Master ID')
    cbt_password = fields.Char(string='CBT Password')
    state = fields.Boolean(string='Active', default=True)
    applicant_line_ids = fields.One2many('applicant.entry.test.line', 'applicant_id')
    description = fields.Html(string='Description')
    slot_type = fields.Selection(
        string='Slot Type',
        selection=[('interviewer', 'Interviewer'),
                   ('test', 'Test'), ],
        required=False, related='entry_test_schedule_details_id.entry_schedule_id.slot_type', store=True)

    @api.depends('applicant_line_ids')
    def _entry_test_marks(self):
        test_marks = 0
        for rec in self:
            for entry in rec.applicant_line_ids:
                test_marks = test_marks + entry.obtained_marks
            rec.entry_test_marks = test_marks

    def section_wise_marks(self):
        merit_application = self.env['odoocms.merit.register.line'].search(
            [('applicant_id', '=', self.student_id.id)])

        if merit_application:
            for rec in self.applicant_line_ids:
                merit_application.write({
                    'cbt_section_ids': [(0, 0, {'name': rec.name, 'marks': rec.obtained_marks})]
                })


class ApplicantEntryTestLine(models.Model):
    _name = 'applicant.entry.test.line'
    _description = 'Applicant Entry Test Line'

    name = fields.Char(string='Name')
    obtained_marks = fields.Integer(string='Obtained Marks')
    total_marks = fields.Integer(string='Total Marks')
    applicant_id = fields.Many2one('applicant.entry.test')
