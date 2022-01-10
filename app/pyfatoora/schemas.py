from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from fastapi import Form
import datetime


class InvoiceData(BaseModel):
    seller_name: str
    tax_number: int
    date: Optional[str] = str(datetime.datetime.now())
    total: Optional[float] = 0.00
    tax_amount: Optional[float] = total * 0.15
