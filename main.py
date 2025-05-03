import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chat_logic import ask_plato, plato_ask_dev
import uvicorn
from fastapi.responses import StreamingResponse


import html


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_home():
    return FileResponse("static/index.html")

@app.get("/debug")
async def serve_debug():
    return FileResponse("static/debug/index.html")


class Query(BaseModel):
    question: str

#Plato

@app.post("/ask")
async def ask_endpoint(query: Query):
    return StreamingResponse(ask_plato(query.question), media_type="text/plain")

@app.post("/debug-ask")
async def debug_ask(query: Query):
    return plato_ask_dev(query.question)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3030, reload=True)



    