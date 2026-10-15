from bson import ObjectId
from bson.errors import InvalidId

from fastapi import FastAPI , UploadFile , File , HTTPException

from app.resume_parser import extract_text_from_pdf

from app.database import resumes_collection
from datetime import datetime, timezone



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

    resume_document = {
    "filename": file.filename,
    "extracted_text": extracted_text,
    "characters_extracted": len(extracted_text),
    "uploaded_at": datetime.now(timezone.utc),
}

    result = resumes_collection.insert_one(resume_document)  

    

    return {
    "message": "Resume uploaded and saved successfully",
    "resume_id": str(result.inserted_id),
    "filename": file.filename,
    "characters_extracted": len(extracted_text),
    "extracted_text": extracted_text,
}

@app.get("/resume/{resume_id}")
def get_resume(resume_id:str):
    try:
        object_id = ObjectId(resume_id)
    except InvalidId:
        raise HTTPException(status_code=400,detail="Invalid Resume ID")

    resume = resumes_collection.find_one(
        {"_id":object_id}

    )

    if resume is None:
        raise HTTPException(status_code=400,detail="Resume not found")

    return {
        "resume_id" : str(resume["_id"]),
        "filename":resume["filename"],
        "characters_extracted": resume["characters_extracted"],
        "uploaded_at": resume["uploaded_at"].isoformat(),
        "extracted_text": resume["extracted_text"]


    }


@app.get("/resumes") 
def get_all_resumes():
    resumes = resumes_collection.find(
        {},  # bring all documents from the database
        {
            "filename": 1,
            "characters_extracted": 1,
            "uploaded_at": 1
        }
    ).sort("uploaded_at", -1)

    return [
        {
            "resume_id": str(resume["_id"]),
            "filename": resume["filename"],
            "characters_extracted": resume["characters_extracted"],
            "uploaded_at": resume["uploaded_at"].isoformat()
        }
        for resume in resumes
    ]


    


