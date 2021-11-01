# api-fatoora
API to help generating QR-code for ZATCA's e-invoice known as Fatoora with any programming language

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

and to generate QR-code
```
/to_qrcode_image/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}
```
