import os
from typing import Optional
from pyfatoora import PyFatoora
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

app = FastAPI()


@app.get("/to_base64/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}")
def base64_endpoint(seller_name, tax_number, invoice_date, total_amount, tax_amount):
    fatoora = PyFatoora(seller_name,
        tax_number,
        invoice_date,
        total_amount,
        tax_amount)

    tlv_as_base64 = fatoora.tlv_to_base64()
    return {"TLV_to_base64": tlv_as_base64}


@app.get("/to_qrcode_image/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}")
def qrcode_image_endpoint(seller_name, tax_number, invoice_date, total_amount, tax_amount, background_tasks: BackgroundTasks):
    fatoora = PyFatoora(seller_name,
        tax_number,
        invoice_date,
        total_amount,
        tax_amount)
    
    qrcode_image = fatoora.render_qrcode_image()
    qrcode_image.save("qr_code_img.png")

    background_tasks.add_task(os.remove, "qr_code_img.png")
    return FileResponse("qr_code_img.png", background=background_tasks)
    
