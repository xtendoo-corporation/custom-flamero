# Copyright 2022 Xtendoo

{
    "name": "Flamero Webservice",
    "summary": """
        Webservice for Flamero Hotels""",
    "version": "15.0.1.0.0",
    "depends": ["mass_mailing", "webservice"],
    "maintainers": ["manuelcalerosolis"],
    "author": "Xtendoo",
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "wizard/webservice_import.xml",
        "views/webservice_import.xml"
    ],
    "application": True,
    "installable": True,
    "auto_install": True,
}
