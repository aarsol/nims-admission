
{
    "name": "Base Rest",
    "summary": """
        Develop your own high level REST APIs for Odoo thanks to this addon.
        pip3 install cerberus
        pip3 install pyquerystring
        pip3 install parse-accept-language
        pip3 install apispec
        pip3 install marshmallow
        pip3 install jsondiff
        pip3 install cachetools
        pip3 install marshmallow-objects
        pip3 install html2text
        pip3 install wheel
        pip install pandas
        """,
    "version": "14.0.3.0.5",
    "development_status": "Beta",
    "license": "LGPL-3",
    "author": "ACSONE SA/NV, " "Odoo Community Association (OCA)",
    "maintainers": ["lmignon"],
    "website": "https://github.com/OCA/rest-framework",
    "depends": ["component"],
    "data": [
        "views/assets_template.xml",
        "views/openapi_template.xml",
        "views/base_rest_view.xml",
    ],
    "demo": [],
    "external_dependencies": {
        "python": [
            "cerberus",
            "pyquerystring",
            "parse-accept-language",
            "apispec>=4.0.0",
        ]
    },
    "installable": True,
}
