import os
from io import BytesIO
import pathlib
import datetime
import random
from typing import Optional
from .pyfatoora import PyFatoora
from .info import InvoiceData
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/to_base64", tags=['tvl to base64'])
async def get_base64_endpoint(
    seller_name: str, 
    tax_number: str,
    total: str,
    tax_amount: str,
    date: Optional[str] = str(datetime.datetime.now())):
    fatoora = PyFatoora(seller_name,
        tax_number,
        date,
        total,
        tax_amount)

    tlv_as_base64 = fatoora.tlv_to_base64()
    return {"TLV_to_base64": tlv_as_base64}

@app.post("/to_base64", tags=['tvl to base64'])
async def post_base64_endpoint(invoice_data : InvoiceData):
    fatoora = PyFatoora(invoice_data.seller_name,
        invoice_data.tax_number,
        invoice_data.invoice_date,
        invoice_data.total_amount,
        invoice_data.tax_amount)

    tlv_as_base64 = fatoora.tlv_to_base64()
    return {"TLV_to_base64": tlv_as_base64}

@app.get("/to_qrcode_image", response_class=FileResponse, tags=['QR-code'])
async def qrcode_image_endpoint(
    seller_name: str, 
    tax_number: str,
    total: str,
    tax_amount: str, 
    background_tasks: BackgroundTasks,
    date: Optional[str] = str(datetime.datetime.now())
    ):

    fatoora = PyFatoora(seller_name,
        tax_number,
        date,
        total,
        tax_amount)
    
    qrcode_image = fatoora.render_qrcode_image()
    qrcode_image.save("qr_code_img.png")

    background_tasks.add_task(os.remove, "qr_code_img.png")
    return FileResponse("qr_code_img.png", background=background_tasks)


@app.post("/to_qrcode_image", response_class=FileResponse, tags=['QR-code'])
async def qrcode_image_endpoint(invoice_data: InvoiceData, background_tasks: BackgroundTasks):
    fatoora = PyFatoora(invoice_data.seller_name,
        invoice_data.tax_number,
        invoice_data.invoice_date,
        invoice_data.total_amount,
        invoice_data.tax_amount)
    
    qrcode_image = fatoora.render_qrcode_image()
    print(type(qrcode_image))
    qrcode_image.save("qr_code_img.png")

    background_tasks.add_task(os.remove, "qr_code_img.png")
    return FileResponse("qr_code_img.png", background=background_tasks)

@app.post("/submitform")
def handle_form(background_tasks: BackgroundTasks,
                    seller_name: str = Form(...), 
                    tax_number: str = Form(...), 
                    invoice_date: str = Form(...),
                    invoice_time: str = Form(...), 
                    total_amount: str = Form(...), 
                    tax_amount: str = Form(...),
                    render_type: str = Form(...)
                ):
    # date = str(invoice_date) + str(invoice_time)
    
    fatoora = PyFatoora(seller_name,
        tax_number,
        invoice_date,
        total_amount,
        tax_amount)
    
    if render_type == "1":
        tlv_as_base64 = fatoora.tlv_to_base64()
        return {"TLV_to_base64": tlv_as_base64}
    
    qrcode_image = fatoora.render_qrcode_image()
    qrcode_image.save("qr_code_img.png")

    # background task to delete the created image from the server
    # after it return to the user
    background_tasks.add_task(os.remove, "qr_code_img.png")
    return FileResponse("qr_code_img.png", background=background_tasks)


@app.post("/read_qrcode_image", status_code=202, tags=['read QR-code image'])
async def read_qrcode_image(image: UploadFile = File(...)):
    if pathlib.Path(image.filename).suffix != ".png":
        raise HTTPException(status_code=415)
    
    pyfat = PyFatoora()
    return pyfat.read_qrcode_image(BytesIO(image.file.read()))

@app.get("/full_fatoora")
async def full_fat(
    request: Request,
    seller_name: str,
    tax_number: str,
    total: str,
    tax_amount: str,
    date: Optional[str] = str(datetime.datetime.now()),
    fat_number: Optional[str] = random.randint(1000, 9999)):

    fatoora = PyFatoora(
        seller_name,
        tax_number,
        date,
        total,
        tax_amount
    )

    data = {
        "fat_number":fat_number,
        "seller_name":seller_name,
        "tax_number": tax_number,
        "date": date,
        "total": total,
        "tax_amount": tax_amount
    }

    return templates.TemplateResponse("fatoora.html", {"request":request, "data":data})