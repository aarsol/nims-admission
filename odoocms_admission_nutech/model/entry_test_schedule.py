import pdb

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class EntryTestSchedule(models.Model):
    _name = 'odoocms.entry.test.schedule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Entry Test Schedule'
    _rec_name = 'entry_test_room_id'

    entry_test_room_id = fields.Many2one('odoocms.entry.test.room', string='Room')
    entry_test_slots_id = fields.Many2one('odoocms.entry.test.slots', string='Slots')
    sequence = fields.Integer('Sequence')
    date = fields.Date(string='Date')
    entry_test_schedule_ids = fields.One2many('odoocms.entry.schedule.details', 'entry_schedule_id')
    count = fields.Integer('Count', compute='_get_applicant_record')
    register_id = fields.Many2one('odoocms.admission.register', string='Register')
    slot_type = fields.Selection(
        string='Slot Type',
        selection=[('interviewer', 'Interviewer'),
                   ('test', 'Test'), ],
        required=False, )

    @api.onchange('entry_test_room_id', 'entry_test_schedule_ids')
    def sum_capacity(self):
        total = 0
        for rec in self:
            for entry in rec.entry_test_schedule_ids:
                total += entry.capacity
                if total > rec.entry_test_room_id.capacity:
                    raise UserError(_("Capacity is full."))

    @api.model
    def create(self, values):
        record = super(EntryTestSchedule, self).create(values)
        if not record.sequence:
            record.sequence = self.env['ir.sequence'].next_by_code('entry.test')
        return record


    # def action_view_candidate(self):
    #     candidates = self.env['applicant.entry.test']
    #     for rec in
    #     if primary_class_ids:
    #         class_list = primary_class_ids.mapped('id')
    #         return {
    #             'domain': [('id', 'in', class_list)],
    #             'name': _('Classes'),
    #             'view_type': 'form',
    #             'view_mode': 'tree,form',
    #             'res_model': 'odoocms.class.primary',
    #             'view_id': False,
    #             'type': 'ir.actions.act_window'
    #         }

    @api.depends('count', 'entry_test_schedule_ids', 'entry_test_schedule_ids.capacity',
                 'entry_test_schedule_ids.count')
    def _get_applicant_record(self):
        for rec in self:
            rec.count = 0
            count_rec = 0
            for entry in rec.entry_test_cshedule_ids:
                subjects = self.env['applicant.entry.test'].search([
                    ('entry_test_schedule_details_id.program_id', '=', entry.program_id.id),
                    ('room', '=', rec.entry_test_room_id.name), ('slots', '=', rec.entry_test_slots_id.id)])

                count_rec = count_rec + entry.count
                rec.count = count_rec

                if entry.status == 'open':
                    entry.count = len(subjects)

                    if entry.capacity == entry.count:
                        entry.status = 'full'

                    else:
                        entry.status = 'open'


class EntryTestScheduleDetails(models.Model):
    _name = 'odoocms.entry.schedule.details'
    _description = 'Entry Test Schedule Details'
    _rec_name = 'program_id'

    capacity = fields.Integer(string='Capacity')
    sequence = fields.Integer('Sequence')
    program_id = fields.Many2one('odoocms.program', string='Program')
    entry_schedule_id = fields.Many2one('odoocms.entry.test.schedule')
    status = fields.Selection(
        string='Status',
        selection=[('open', 'Open'),
                   ('initialize', 'Initialize'),
                   ('full', 'Full'), ('close', 'Close')
                   ],
        default='open')
    count = fields.Integer('Count')

    @api.model
    def create(self, values):
        record = super(EntryTestScheduleDetails, self).create(values)
        if not record.sequence:
            record.sequence = self.env['ir.sequence'].next_by_code('entry.test')
        return record
