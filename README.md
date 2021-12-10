# api-fatoora

<p align="center">
  <img align="center" src="https://github.com/NafieAlhilaly/api-fatoora/blob/main/images/full_E-invoice.jpg" width=300/>
</p>

You can try it with simple ui @ [api-fatoora](https://api-fatoora.herokuapp.com/)


api-fatoora is an open API to help generating QR-code for [ZATCA's e-invoice known as "Fatoorah"](https://zatca.gov.sa/en/E-Invoicing/Introduction/Pages/What-is-e-invoicing.aspx) with any programming language




full API [documentations](https://api-fatoora.herokuapp.com/docs) 


---------
## how to use it 

lets say you have the following data 
```json
{
  "seller_name":"Nafie",
  "tax_number":"981293479834",
  "date":"2021-12-06 16:14:17.374909",
  "total_amount":"100.00",
  "tax_amount":"0.50"
}
```

### To base64
Use /to_base64 to get base64 encoded information
```
Parameter :
  seller_name: required
  tax_number: required
  date: optional, if not provided created date and time will be added
  total: required
  tax_amount: required
  
  
https://api-fatoora.herokuapp.com/to_base64?seller_name=Nafie&tax_number=981293479834&total=100.00&tax_amount=0.50&date=2021-12-06%2016%3A14%3A17.374909
```
[Try it](https://api-fatoora.herokuapp.com/to_base64?seller_name=Nafie&tax_number=981293479834&total=100.00&tax_amount=0.50&date=2021-12-06%2016%3A14%3A17.374909)

### To QR-Code image
Use /to_qrcode_image to generate QR-COde image
```
Parameter :
  seller_name: required
  tax_number: required
  date: optional, if not provided created date and time will be added
  total: required
  tax_amount: required
  
  

https://api-fatoora.herokuapp.com/to_qrcode_image?seller_name=Nafi&tax_number=981293479834&total=100.00&tax_amount=0.50&date=2021-12-06%2016%3A14%3A17.374909
```
[Try it](https://api-fatoora.herokuapp.com/to_qrcode_image?seller_name=Nafi&tax_number=981293479834&total=100.00&tax_amount=0.50&date=2021-12-06%2016%3A14%3A17.374909
)

### Fill E-Invoice(fatoora)
Use /full_fatoora to get e-invoice with qrcode image
```
Parameter :
  fat_number: Optional, e-ivoice number/id if not ptovided it will be filled with random numbers
  seller_name: required
  tax_number: required
  date: optional, if not provided created date and time will be added
  total: required
  tax_amount: required
  
  

https://api-fatoora.herokuapp.com/full_fatoora?seller_name=Nafie&tax_number=981293479834&total=100.00&tax_amount=0.50&date=2021-12-06%2016%3A14%3A17.374909&fat_number=5837

```
[Try it](https://api-fatoora.herokuapp.com/full_fatoora?seller_name=Nafie&tax_number=981293479834&total=100.00&tax_amount=0.50&date=2021-12-06%2016%3A14%3A17.374909&fat_number=5837
)


