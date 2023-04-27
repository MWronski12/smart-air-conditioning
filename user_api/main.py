import uvicorn
from app import app
from app.config import FAST_API_HOST, FAST_API_PORT

if __name__ == "__main__":
    uvicorn.run(app, host=FAST_API_HOST, port=FAST_API_PORT)
