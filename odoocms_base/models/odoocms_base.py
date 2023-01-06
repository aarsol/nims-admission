import pdb
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class OdooCMSReligion(models.Model):
    _name = 'odoocms.religion'
    _description = 'Religion'
    _order = 'sequence'

    name = fields.Char(string="Religion", required=True)
    code = fields.Char(string="Code", required=True)
    sequence = fields.Integer(string='Sequence')
    color = fields.Integer('Color')
    

class OdooCMSCity(models.Model):
    _name = 'odoocms.city'
    _description = 'City'
    _order = 'sequence'

    name = fields.Char(string="City", required=True)
    code = fields.Char(string="City Code", required=True)
    sequence = fields.Integer(string='Sequence')


class OdooCMSProvince(models.Model):
    _name = 'odoocms.province'
    _description = 'Province'
    _order = 'sequence'

    country_id = fields.Many2one('res.country', string="Country")
    name = fields.Char(string="Province", required=True)
    code = fields.Char(string="Code", required=True)
    sequence = fields.Integer(string='Sequence')
    domicile_ids = fields.One2many('odoocms.domicile', 'province_id', string='Domiciles')
    district_ids = fields.One2many('odoocms.district', 'province_id', string="Districts")


class OdooCMSDistrict(models.Model):
    _name = 'odoocms.district'
    _description = 'District'
    _order = 'sequence'

    province_id = fields.Many2one('odoocms.province', string="Province")
    name = fields.Char('District Name',size=32, required=True)
    code = fields.Char('Code', size=8, required=True)
    sequence = fields.Integer(string='Sequence')


class OdooCMSDomicile(models.Model):
    _name = 'odoocms.domicile'
    _description = 'Domicile'
    _order = 'sequence'

    name = fields.Char(string="Domicile Region", required=True)
    code = fields.Char(string="Code", required=True)
    province_id = fields.Many2one('odoocms.province', string='Province')
    sequence = fields.Integer(string='Sequence')


class OdooCMSMartialStatus(models.Model):
    _name = 'odoocms.marital.status'
    _description = 'Marital Status'
    _order = 'sequence'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    sequence = fields.Integer(string='Sequence')
    color = fields.Integer('Color')
    

class OdooCMSProfession(models.Model):
    _name = 'odoocms.profession'
    _description = 'Profession'
    _order = 'sequence'

    code = fields.Char(string="Code", help="Code")
    name = fields.Char(string="Name", required=False, )
    sequence = fields.Integer(string='Sequence')
    apply_on = fields.Selection([('m','Male'),('f','Female'),('b','Both')], 'Apply on', default='b')
   

class OdooCMSLanguage(models.Model):
    _name = 'odoocms.language'
    _description = "OdooCMS Languages"

    name = fields.Char('Name')
    code = fields.Char('Code')
    sequence = fields.Integer(string='Sequence')


class OdooCMSCareer(models.Model):
    _name = "odoocms.career"
    _description = "CMS Career"
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    to_be = fields.Boolean(default=False)
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super(OdooCMSCareer, self).name_search(name, args=args, operator=operator, limit=limit)