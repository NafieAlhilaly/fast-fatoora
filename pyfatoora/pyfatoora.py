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
from uttlv import TLV
import base64
import qrcode
import cv2


class PyFatoora:
    """
    This class will help transform given seller information 
    to a QR-code image as part of ZATCA requirements for implementation of
    e-invoice (fatoora).
    """
    tags = TLV()

    def __init__(self, seller_name: str,
                 tax_number: str,
                 invoice_date: str,
                 total_amount: str,
                 tax_amount: str):
        self.seller_name = seller_name
        self.tax_number = tax_number
        self.invoice_date = invoice_date
        self.total_amount = total_amount
        self.tax_amount = tax_amount

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

    def read_qrcode_image(self, image_url:str, dictionary=True) -> str or dict:
        """
        extract seller information from qr-code image.

        :param image_url: 
            a qr-code image path or url
        :param dictionary: 
            return result as a dictionary if True,
            else return base64 code.
        :return: 
            str base64 code, or 
            dictionary contains seller information
        """
        # read the QRCODE image
        image = cv2.imread(image_url)

        # initialize the cv2 QRCode detector
        detector = cv2.QRCodeDetector()

        if image :
            # detect and decode
            data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
        else:
            return "ivalid image url"
        
        if dictionary:
            return self.decode_tlv(data)
        else:
            return data
