{
    "name": "Importation from XML",
    "category": "Project",
    "version": "15.0.1.0",
    "depends": ["base","mass_mailing"],
    "description": """
        Wizard to Import from XML files.
        """,
    "data": [
        "security/ir.model.access.csv",
        "wizard/xml_flamero_import.xml",
        "views/xml_flamero_import.xml"
    ],
    'application': True,
    "installable": True,
    "auto_install": True,
}
