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
        try:
            xml_root = etree.fromstring(file_data)
        except Exception as e:
            raise UserError(_("This XML file is not XML-compliant. Error: %s") % e)

        for entry in xml_root.xpath('ns:entry', namespaces={"ns": "http://www.w3.org/2005/Atom"}):
            content = entry.find('{http://www.w3.org/2005/Atom}content')
            properties = content.xpath("m:properties", namespaces={
                "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})
            email = properties[0].xpath("d:E_mail", namespaces={
                "d": "http://schemas.microsoft.com/ado/2007/08/dataservices"})
            if email is not None:
                nombre = properties[0].xpath("d:Nombre",
                                            namespaces={"d": "http://schemas.microsoft.com/ado/2007/08/dataservices"})
                print("*"*80)
                print("email", email[0].text)
                print("nombre", nombre[0].text)
                print("*"*80)

    def import_file(self):
        self.ensure_one()
        self.get_parsed_invoice(self.invoice_file)
