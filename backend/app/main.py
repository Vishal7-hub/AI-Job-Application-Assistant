
from fastapi import FastAPI , UploadFile , File , HTTPException

from app.resume_parser import extract_text_from_pdf


app = FastAPI(
    title="AI job Application Assistant",
    description="An AI powered Resume and job matching platform",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"message":"AI Job Application Assistant API is working "}

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/resume/upload")
async def upload_resume(file : UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith("pdf"):
        raise HTTPException(
            status_code = 404,
            detail="only pdf files are allowed"

        )
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty"

        )

    try:
        extracted_text = extract_text_from_pdf(file_bytes)

    except ValueError as exc :
        raise HTTPException(status_code=422 , detail=str(exc))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="could not read this PDF. Please upload a valid pdf file"
        )

    return {
        "filename":file.filename,
        "characters_extracted":len(extracted_text),
        "extracted_text":extracted_text,
    }

