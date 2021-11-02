<p align="center">
  <img align="center" src="https://github.com/NafieAlhilaly/api-fatoora/blob/main/images/secret-qr-code.png" width=300/>
</p>

You can try it @ [api-fatoora](https://api-fatoora.herokuapp.com/)
# api-fatoora
API to help generating QR-code for ZATCA's e-invoice known as Fatoora with any programming language

> _Disclaimer: this API is not **secure** yet, please dont share sensitive information._

---------
## how to use it 
Basicly you can get the result as json from any language with a simple http request.
```
# base api
https://api-fatoora.herokuapp.com/

# base64 converting endpoint
to_base64/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}

# full base64 url
https://api-fatoora.herokuapp.com/to_base64/Nafie,1234567893,2021-07-12T14:25:09Z,120.00,20.00


# qr-code endpoint
/to_qrcode_image/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}

# full qr-code endpoint
https://api-fatoora.herokuapp.com/to_qrcode_image/Nafie,1234567893,2021-07-12T14:25:09Z,120.00,20.00
```

🔗[try base64](https://api-fatoora.herokuapp.com/to_base64/Nafie,1234567893,2021-07-12T14:25:09Z,120.00,20.00)

🔗[try QR-code](https://api-fatoora.herokuapp.com/to_qrcode_image/Nafie,1234567893,2021-07-12T14:25:09Z,120.00,20.00)


------------

getting base64 using python 
```
import requests

# invoice/seller information
seller_name = "Salla"
tax_number = "1234567891"
invoice_date = "2021-07-12T14:25:09Z"
total_amount = "100.00"
tax_amount ="15.00"

res = requests.get(f"https://api-fatoora.herokuapp.com/to_base64/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}")
print(res.json())
```
expected output 
```
{'TLV_to_base64': 'AQVTYWxsYQIKMTIzNDU2Nzg5MQMUMjAyMS0wNy0xMlQxNDoyNTowOVoEBjEwMC4wMAUFMTUuMDA='}
```
