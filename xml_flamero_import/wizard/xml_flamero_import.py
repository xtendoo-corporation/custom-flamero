import base64
import logging
from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)

class XmlFlameroImport(models.TransientModel):
    _name = "xml.flamero.import"
    _description = "Importador Xml Flamero"

    data_file_xml = fields.Binary(
        string="File to Import",
        required=False,
        help="Get you data from xml file.",
    )
    invoice_file = fields.Binary(
        string="PDF or XML Invoice"
    )
    invoice_filename = fields.Char(
        string="Filename"
    )

    @api.model
    def get_parsed_invoice(self, invoice_file_b64):
        assert invoice_file_b64, "No invoice file"
        assert isinstance(invoice_file_b64, bytes)
        file_data = base64.b64decode(invoice_file_b64)

        print("*"*80)
        print("file_data:", file_data)
        print("*"*80)

        try:
            xml_root = etree.fromstring(file_data)
        except Exception as e:
            raise UserError(_("This XML file is not XML-compliant. Error: %s") % e)

        pretty_xml_bytes = etree.tostring(
                xml_root, pretty_print=True, encoding="UTF-8", xml_declaration=True
            )

        for element in xml_root:
            print("*" * 80)
            print("element:", element)
            for e in element:
                print("e:", e)
            print("*" * 80)

        print("*"*80)
        print("pretty_xml_bytes:", pretty_xml_bytes)
        print("*"*80)

    def import_file(self):
        self.ensure_one()
        self.get_parsed_invoice(self.invoice_file)
