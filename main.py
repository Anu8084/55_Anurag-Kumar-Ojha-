from fastapi import FastAPI, UploadFile
from pdf_loader import load_pdf
from rag import create_vectorstore, ask_question
from image_bot import analyze_image
from PIL import Image
import io

app = FastAPI()

VECTORSTORE = None

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile):
    global VECTORSTORE
    text = load_pdf(file.file)
    VECTORSTORE = create_vectorstore(text)
    return {"status": "PDF indexed successfully"}

@app.post("/ask-pdf")
async def ask_pdf(question: str, system_prompt: str):
    if VECTORSTORE is None:
        return {"error": "Upload PDF first"}
    answer = ask_question(VECTORSTORE, question, system_prompt)
    return {"answer": answer}

@app.post("/image-qa")
async def image_qa(file: UploadFile, question: str):
    image = Image.open(io.BytesIO(await file.read()))
    answer = analyze_image(image, question)
    return {"answer": answer}
