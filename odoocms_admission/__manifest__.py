# -*- coding: utf-8 -*-


{
    'name': "OdooCMS Admission",
    'version': '14.0',
    'license': 'LGPL-3',
    'category': 'OdooCMS',
    'sequence': 3,
    'summary': "Admission Module of Educational""",
    'author': 'AARSOL',
    'company': 'AARSOL',
    'website': "http://www.aarsol.com/",
    'depends': ['odoocms_base', 'mail', 'odoocms'],
    'data': [
        'security/odoocms_admission_security.xml',
        'security/ir.model.access.csv',

        'data/admission_mail_template.xml',
        # 'data/data.xml',
        'menus/odoocms_admission_menu.xml',
        'views/sequence.xml',
        'views/admission_register_view.xml',
        'views/odoocms_application_view.xml',
        # 'views/odoocms_merit_list.xml',
        'views/odoocms_admission_common.xml',
        'views/test_schedule.xml',
        'views/test_series.xml',
        'views/register_candidate_view.xml',
        'views/odoocms_admission_education.xml',

        'views/odoocms_admission_degree.xml',
        'views/odoocms_admission_specialization.xml',
        'views/degree_subject_detail.xml',
        'views/pre_test_view.xml',
        'views/admission_documents.xml',
        # 'views/odoocms_overall_result.xml',

        'wizard/success_message_wizard_view.xml',

    ],
    'demo': [
        # 'demo/admission_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
