# api-fatoora

<p align="center">
  <img align="center" src="https://github.com/NafieAlhilaly/api-fatoora/blob/main/images/full_E-invoice.jpg" width=300/>
</p>

You can try it with simple ui @ [api-fatoora](https://api-fatoora.herokuapp.com/)


api-fatoora is an open API to help generating QR-code for [ZATCA's e-invoice known as "Fatoorah"](https://zatca.gov.sa/en/E-Invoicing/Introduction/Pages/What-is-e-invoicing.aspx) with any programming language

---------
## how to use it 
The simplest way to get started is to send POST request with json of your data, here an example using python requests

#### Convert data to base 64
`POST /to_base64/`
```python
import requests
import json

data = {
    "seller_name": "nafie",
    "tax_number": "876554674",
    "invoice_date": "875t6554",
    "total_amount": "200",
    "tax_amount": "30"   
}

data = json.dumps(data)

response = requests.post('https://api-fatoora.herokuapp.com/to_base64', data=data)
print(response.json())
# result : {'TLV_to_base64': 'AQVuYWZpZQIJODc2NTU0Njc0Awg4NzV0NjU1NAQDMjAwBQIzMA=='}
```

#### Convert data to QR-Code
`POST /to_qrcode_image/`
```python
from PIL import Image
import io
import requests
import json

data = {
    "seller_name": "nafie",
    "tax_number": "876554674",
    "invoice_date": "875t6554",
    "total_amount": "200",
    "tax_amount": "30"   
}

data = json.dumps(data)
response = requests.post('http://127.0.0.1:8000/to_qrcode_image', data=data)

# get image response as bytes
image_data = response.content

# convert bytes to image using PIL.Image
image = Image.open(io.BytesIO(image_data))
image.show()
```
