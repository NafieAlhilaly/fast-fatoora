"""
A module to implement ZATCA e-invoice (fatoora)
it will convert seller information to TLV tags, 
then to hexadecimal representation finally to base64 encoding.

from base64 encoding result we can render RQ-code

The minimum seller inforamion required are :

- Seller’s name.
- Seller’s tax number.
- Invoice date.
- Invoice total amount.
- Tax amount.

"""
from typing import Optional
from uttlv import TLV
import base64
import qrcode
import cv2
from PIL import Image
from pyzbar.pyzbar import decode


class PyFatoora:
    """
    This class will help transform given seller information 
    to a QR-code image as part of ZATCA requirements for implementation of
    e-invoice (fatoora).
    """
    tags = TLV()
    seller_name: Optional[str] = None
    tax_number: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[str] = None
    tax_amount: Optional[str] = None

    def __init__(self, 
                 seller_name: Optional[str] = None,
                 tax_number: Optional[str] = None,
                 invoice_date: Optional[str] = None,
                 total_amount: Optional[str] = None,
                 tax_amount: Optional[str] = None):
        self.set_info(
            seller_name=seller_name,
            tax_number=tax_number,
            invoice_date=invoice_date,
            total_amount=total_amount,
            tax_amount=tax_amount
        )

    def set_info(
        self,
        seller_name: Optional[str] = seller_name,
        tax_number: Optional[str] = tax_number,
        invoice_date: Optional[str] = invoice_date,
        total_amount: Optional[str] = total_amount,
        tax_amount: Optional[str] = total_amount) -> None:

        self.seller_name = seller_name
        self.tax_number = tax_number
        self.invoice_date = invoice_date
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        

    def get_info(self) -> dict:
        
        info: dict = {
            "seller_name": self.seller_name,
            "tax_number": self.tax_number,
            "invoice_date": self.invoice_date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount
        }
        return info

    def tlv_to_base64(self) -> dict:
        """
        convert object tags to byte array then apply base 64 encode on tlv list
        :return: dict: tlv list and base 64 encoded tlv list
        """
        self.tags[0x01] = self.seller_name
        self.tags[0x02] = self.tax_number
        self.tags[0x03] = self.invoice_date
        self.tags[0x04] = self.total_amount
        self.tags[0x05] = self.tax_amount

        tlv_as_byte_array = self.tags.to_byte_array()

        tlv_as_base64 = base64.b64encode(tlv_as_byte_array)
        tlv_as_base64 = tlv_as_base64.decode("ascii")

        return tlv_as_base64


    def render_qrcode_image(self) -> qrcode:
        """
        render base64 tlv result to a QR-code image

        :return: None
        """
        base64_tlv = self.tlv_to_base64()
        qr_code_img = qrcode.make(base64_tlv)
        return qr_code_img

    def base64_to_tlv(self, base64_string: str) -> dict:
        """
        decode tlv values to string and return a dict

        :param: base64_string: tlv tags as base64
        :return: dict
        """
    
        decoded_tlv_data = base64.b64decode(base64_string)

        tags = TLV()
        tags.parse_array(bytes(decoded_tlv_data))

        seller_info = {}
        for tag in tags:
            tag_value = str(tags[tag]).replace("b'", "").replace("'", "")
            seller_info[str(tag)] = tag_value
        return seller_info

    def read_qrcode_image(self, image_url:str) -> str or dict:
        """
        extract seller information from qr-code image.

        :param image_url: 
            a qr-code image path or url
        
        :return:
            dictionary contains decoded seller information
        """
        data = decode(Image.open(image_url))
        extracted_info = self.base64_to_tlv(data[0][0])

        return extracted_info
