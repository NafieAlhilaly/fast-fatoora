from api.api_v1.api import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_main_endpoint():
    """Test main root"""

    response = client.get("/")

    assert response.status_code == 200


def test_404():
    """Test non-existed root"""

    response = client.get("/any")

    assert response.status_code == 404


def test_qrcode_image_endpoint_without_inputs():
    """Test with missing data or if the resuest was GET instead of POST"""
    response = client.post("/to_qrcode_image")

    assert response.status_code == 422


def test_qrcode_image_endpoint():
    """Test with expected data"""

    data = {
        "seller_name": "Nafie",
        "tax_number": "49823534234",
        "invoice_date": "3465768",
        "total_amount": "972.1",
        "tax_amount": "99.99",
    }

    response = client.post("/to_qrcode_image", json=data)

    assert response.status_code == 200


def test_handle_form_missing_data():
    """Test dandling missing form data"""

    response = client.post("/submitform")

    assert response.status_code == 422
