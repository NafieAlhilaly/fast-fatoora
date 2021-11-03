import os
from typing import Optional
from pyfatoora import PyFatoora
from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# cors configuration for all ports
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.post("/submitform")
async def handle_form(seller_name: str = Form(...), 
                    tax_number: str = Form(...), 
                    invoice_date: str = Form(...),
                    invoice_time: str = Form(...), 
                    total_amount: str = Form(...), 
                    tax_amount: str = Form(...),
                    render_type: str = Form(...)):
    date = str(invoice_date) + str(invoice_time)
    if render_type == "1":
        response = RedirectResponse(url= "/to_base64/{seller_name},{tax_number},{date},{total_amount},{tax_amount}")
        response.status_code = 302
        return response

    response = RedirectResponse(url= "/to_qrcode_image/{seller_name},{tax_number},{invoice_date},{total_amount},{tax_amount}")
    response.status_code = 302
    return response

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
    
