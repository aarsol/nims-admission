# -*- encoding: utf-8 -*-
{
    'name': 'Application Portal',
    'summary': 'OdooCms Application Portal For Admission.',
    'category': 'OdooCMS',
    'version': '14.0',
    'license': 'LGPL-3',
    'category': 'OdooCMS',
    'sequence': 4,
    'author': 'AARSOL',
    'company': 'AARSOL',
    'website': 'http://www.aarsol.com/',
    'depends': ['odoocms_admission','website'],
    'data': [
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'views//backend/res_config_settings_views.xml',
        'views/backend/odoocms_application_main_step_view.xml',
        'views/portal/component/header.xml',
        'views/portal/component/carousel.xml',
        'views/portal/component/progress.xml',
        'views/backend/odoocms_application_view.xml',
        'views/portal/submission_message.xml',
        'views/portal/admission_application.xml',
        'views/portal/steps/personal_details.xml',
        'views/portal/steps/preferences.xml',
        'views/portal/steps/final_confirmation.xml',
        'views/portal/steps/testing_center.xml',
        'views/portal/steps/fee_voucher.xml',
        'views/portal/steps/documents_upload.xml',
        'views/portal/steps/contact_details.xml',
        'views/portal/steps/quota.xml',
        'views/portal/steps/test_center_nutech.xml',
        'views/portal/steps/guardian_details.xml',
        'views/portal/steps/scholarship.xml',
        'views/portal/steps/merit.xml',
        'views/portal/steps/program_transfer.xml',
        'views/portal/steps/education_details.xml',
        'views/portal/account_registration.xml',
        'views/portal/all_merit.xml',
        'views/portal/dashboard.xml',

        'reports/report_admission_invoice.xml',
        'reports/admit_card.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
