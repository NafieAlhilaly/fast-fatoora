import os
from .pyfatoora import PyFatoora
from .info import InvoiceData
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

@app.post("/to_base64")
async def base64_endpoint(invoice_data : InvoiceData):
    fatoora = PyFatoora(invoice_data.seller_name,
        invoice_data.tax_number,
        invoice_data.invoice_date,
        invoice_data.total_amount,
        invoice_data.tax_amount)

    tlv_as_base64 = fatoora.tlv_to_base64()
    return {"TLV_to_base64": tlv_as_base64}

@app.post("/to_qrcode_image")
async def qrcode_image_endpoint(invoice_data: InvoiceData, background_tasks: BackgroundTasks):
    fatoora = PyFatoora(invoice_data.seller_name,
        invoice_data.tax_number,
        invoice_data.invoice_date,
        invoice_data.total_amount,
        invoice_data.tax_amount)
    
    qrcode_image = fatoora.render_qrcode_image()
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

    date = str(invoice_date) + str(invoice_time)
    
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

    background_tasks.add_task(os.remove, "qr_code_img.png")
    return FileResponse("qr_code_img.png", background=background_tasks)
