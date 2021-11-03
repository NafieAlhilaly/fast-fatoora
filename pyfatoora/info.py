from typing import Optional
from pydantic import BaseModel

class InvoiceData(BaseModel):
    seller_name: str 
    tax_number: str
    invoice_date: str
    total_amount: str
    tax_amount: str