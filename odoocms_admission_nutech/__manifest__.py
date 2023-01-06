# -*- coding: utf-8 -*-
{
    'name': "OdooCMS Admission Nutech",
    'version': '14.0',
    'license': 'LGPL-3',
    'category': 'OdooCMS',
    'sequence': 3,
    'summary': "Admission Module of Educational""",
    'author': 'Yasir',
    'company': 'AARSOL',
    'website': "http://www.aarsol.com/",
    'depends': ['odoocms_base', 'mail', 'odoocms_admission'],
    'data': [
        # 'security/odoocms_admission_security.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'data/mail_template.xml',

        # 'views/pgc_institute_view.xml',
        # 'views/pgc_scholarship_view.xml',
        'views/educational_institute.xml',


        'views/entry_test_room_view.xml',
        'views/entry_test_slots_view.xml',
        'views/entry_test_schedule_view.xml',
        'views/applicant_entry_test.xml',
        # 'views/Program_transfer_request.xml',
        # 'views/last_institute_attend_view.xml',
        'views/odoocms_advertisement_view.xml',
        'views/inherit_odoocms_application_view.xml',
        'views/offer_letter.xml',

        'reports/report.xml',
        'reports/admit_card.xml',
        'reports/interview_admit_card.xml',
        'reports/offer_letter.xml',
        'views/generate_admit_card.xml',

        #help desk
        'views/admission_helpdesk.xml',

    ],
    'demo': [
        # 'demo/admission_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
