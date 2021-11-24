from pyfatoora.api import app
from fastapi.responses import FileResponse
from pyfatoora.info import InvoiceData
from fastapi.testclient import TestClient


client = TestClient(app)

def test_main_endpoint():
    """Test main root"""

    response = client.get("/")

    assert response.status_code == 200

def test_404():
    """ Test non-existed root"""

    response = client.get("/any")

    assert response.status_code == 404

def test_qrcode_image_endpoint():
    """ Test enpoint without geving it information"""
    response = client.post("/to_qrcode_image")

    assert response.status_code == 422