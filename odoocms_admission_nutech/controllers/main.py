from odoo.http import route, request, Controller
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
import json


class Cbt(Controller):

    @route('/entry/test/', type='json', auth='user', csrf=False)
    def entry_test(self, **kw):
        try:
            entry_test = request.env['applicant.entry.test'].sudo().search([
                ('state', '=', True)])
            data = []
            for rec in entry_test:
                first_name = rec.student_id.first_name if rec.student_id.first_name else ''
                last_name = rec.student_id.last_name if rec.student_id.last_name else ''
                middle_name = rec.student_id.middle_name if rec.student_id.middle_name else ''
                name = f"{first_name} {middle_name} {last_name}"
                record = {
                    'name': name,
                    'application_no': rec.student_id.application_no,
                    'password': rec.cbt_password,
                    'program_id': json.dumps({'code': rec.student_id.preference_ids.filtered(lambda x : x.preference == 1 ).program_id.code or False ,'name': rec.student_id.preference_ids.filtered(lambda x : x.preference == 1 ).program_id.name or False  }) or False,
                    'cid':rec.id,
                    'slot': json.dumps(
                        {'time_from': rec.slots.time_from, 'time_to': rec.slots.time_to,
                         'name': rec.slots.name}) or False,
                    'room': rec.room.name if rec.room else False,
                    'date': datetime.strftime(rec.date, '%Y-%m-%d') if rec.date else False,
                    'master_id': rec.master_id if rec.master_id else False,
                }

                data.append(record)
            return json.dumps(data)
        except Exception as e:
            return json.dumps({'error': f'{e}'})

    @route('/result/import/', type='json', auth='user', csrf=False)
    def import_result(self, **kw):
        try:

            if request.httprequest.method == 'POST':
                for result in json.loads(kw.get('result_all')):
                    application_no = list(result.keys())[0]
                    application_cid = list(result.values())[1]
                    subject_dict = list(result.values())[0]
 
                    # application_id = request.env['odoocms.application'].sudo().search(
                    #     [('id', '=', application_cid)])
                    student_entry_test = request.env['applicant.entry.test'].sudo().search(
                        [('id', '=', application_cid)])
                    if student_entry_test:
                        for k, v in subject_dict.items():
                            subject_name = k
                            subject_score = v['subject_score']
                            subject_total_score = v['subject_total_score']
                            student_entry_test.applicant_line_ids.create({
                                'applicant_id': student_entry_test.id,
                                'name': subject_name,
                                'obtained_marks': subject_score,
                                'total_marks': subject_total_score,
                            })
                return json.dumps({
                    'status':'yes'
                })
        except Exception as e:
            return json.dumps({
                'status':'no',
                'error': f'{e}'})
