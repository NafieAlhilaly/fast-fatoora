from pyfatoora.api import app
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