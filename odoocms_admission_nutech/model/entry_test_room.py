import pdb

from odoo import fields, models, _, api


class EntryTestRoom(models.Model):
    _name = 'odoocms.entry.test.room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Entry Test Room'

    name = fields.Char(string='Room Name')
    code = fields.Char(string='Code')
    capacity = fields.Integer(string='Capacity')
