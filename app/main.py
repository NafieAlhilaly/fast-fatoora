from api.api_v1.api import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app)
