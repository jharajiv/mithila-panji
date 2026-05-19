import traceback
from typing import List
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from config import origins
from ApiServices.panjiservices import query_panji_database, add_new_document, query_uploaded_documents, load_panji_database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/load")
async def load_documents(files: List[UploadFile] = File(...)):
    try:
        for file in files:
            file_data = await file.read()
            result = await add_new_document(file_data, file.filename)  # Pass the content and filename to the add_new_document function
            return result
    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail={"error": f"Error processing file: {str(e)}"})


@app.post("/api/querynewdocuments")
async def query(query_text: str):
    try:
        result = await query_uploaded_documents(query_text=query_text)
        return {"result": result}
    except Exception as e:
        print(f"Error querying documents: {e}")
        raise HTTPException(status_code=500, detail={"error": f"Error querying documents: {str(e)}"})

@app.post("/api/querypanjidatabase")
async def query(query_text: str):
    try:
        result = await query_panji_database(query_text=query_text)
        return {"result": result}
    except Exception as e:
        print(f"Error querying documents: {e,traceback.format_exc()}")
        raise HTTPException(status_code=500, detail={"error": f"Error querying documents: {e}"})
    


if __name__ == "__main__":
    
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
