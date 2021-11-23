from pyfatoora.api import app
from fastapi.testclient import TestClient


client = TestClient(app)
