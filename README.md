<p align="center">
  <img align="center" src="https://github.com/NafieAlhilaly/api-fatoora/blob/main/images/secret-qr-code.png" width=300/>
</p>


# api-fatoora
API to help generating QR-code for ZATCA's e-invoice known as Fatoora with any programming language

_Disclaimer: this API is not **secure** yet, please dont share sensitive information._

---------
## how to use it 
the base is 
```
https://api-fatoora.herokuapp.com/
```

after you can add 
```
  to_base64/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}
```
to convert information to base64 encode
```
  https://api-fatoora.herokuapp.com/to_base64/Nafie,1234567893,2021-07-12T14:25:09Z,120.00,20.00
```
[try it](https://api-fatoora.herokuapp.com/to_base64/Nafie,1234567893,2021-07-12T14:25:09Z,120.00,20.00)

------------------
and to generate QR-code
```
/to_qrcode_image/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}
```
```
https://api-fatoora.herokuapp.com/to_qrcode_image/Nafie,1234567893,2021-07-12T14:25:09Z,120.00,20.00
```
[try it](https://api-fatoora.herokuapp.com/to_qrcode_image/Nafie,1234567893,2021-07-12T14:25:09Z,120.00,20.00)


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
