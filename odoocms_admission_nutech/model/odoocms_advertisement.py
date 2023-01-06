import pdb

from odoo import fields, models, _, api


class OdooCmsAdvertisement(models.Model):
    _name = 'odoocms.advertisement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Odoo CMS Adevertisement'
    _rec_name = 'advertisement'

    advertisement = fields.Char(string='How do You Know about us?')
