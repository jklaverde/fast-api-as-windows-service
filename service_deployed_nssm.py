
from fastapi import FastAPI
import uvicorn
import multiprocessing

app = FastAPI()


@app.get("/")
def read_root():
    return ("Service deployed as executable not installed as a service yet")


if __name__ == "__main__":
    multiprocessing.freeze_support_support()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)