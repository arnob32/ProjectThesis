from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Hello, Exam Grading System!</h1><p>FastAPI is running 🎉</p>"
