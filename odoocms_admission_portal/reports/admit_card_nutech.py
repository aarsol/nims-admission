import pdb
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone, utc
import pytz
import time
import logging
_logger = logging.getLogger(__name__)


class StudentExamSlip(models.AbstractModel):
    _name = 'report.odoocms_admission_portal.applicant_admit_card_report'
    _description = 'Applicant Admit Card Report'

    @api.model
    def _get_report_values(self, docsid, data=None):
        if docsid:
            company_id = self.env.user.company_id
            # current_user = http.request.env.user
            #

            applicant = self.env['odoocms.application'].sudo().browse(docsid)
            register = self.env['odoocms.admission.register'].sudo().search([('state', '=', 'application')])
            program_preferences_ordered = self.env['odoocms.application.preference'].sudo().search(
                [('application_id', '=', applicant.id)], order='preference asc')
            selected_discipline = []
            for program in program_preferences_ordered:
                selected_discipline += program.discipline_id
            selected_discipline = list(dict.fromkeys(selected_discipline))

            # for i in range(0, len(selected_discipline)):
            #     selected_discipline[i] = int(selected_discipline[i])
            # term_id = self.env['odoocms.datesheet'].search([],order='number desc',limit=1).term_id.id
            docargs = {
                'applicant': applicant,
                'company_id': company_id,
                'pak_time': datetime.now(pytz.timezone('Asia/Karachi')).strftime('%d-%m-%Y %H:%M:%S'),
                'register': register[0],
                'selected_discipline': selected_discipline

                # 'application_ids': application_ids or False,
                # 'account_payable': account_payable or "",
                # 'account_payable2': account_payable2 or "",
                # 'registration_fee': registration_fee or False,
                # 'additional_fee': additional_fee or False,
                # 'total_fee': str(total_fee),
                # 'registration_fee_international': registration_fee_international or False,
                # 'account_title': account_title or "",
                # 'account_title2': account_title2 or "",
                # 'account_no': account_no or "",
                # 'account_no2': account_no2 or "",
                # 'disciplines': disciplines,
                # 'today': date.today() or False,
            }
            return docargs