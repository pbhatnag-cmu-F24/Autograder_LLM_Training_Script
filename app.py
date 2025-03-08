from flask import Flask
from scripts.process_zip_files import create_dataset
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Union
import zipfile
import os
import json
import shutil
import tempfile
import ast
import re
from pathlib import Path
import boto3
import PyPDF2
import uvicorn


#app = Flask(__name__)
app2 = FastAPI(title="Code Extraction and Mapping API")

class FilterConfig(BaseModel):
    filter_out: Optional[List[str]] = []
    file: Optional[List[str]] = []
    division: Optional[Dict[str, Any]] = {"file": True, "method": False, "class": False, "line": False}
    file_extension_filter: Optional[List[str]] = []
    file_extension_filter_type: Optional[str] = "in"
    filename_filter_in: Optional[List[str]] = []
    filename_filter_type: Optional[str] = "in"
    methodname_filter: Optional[List[str]] = []
    methodname_filter_type: Optional[str] = "in"
    classname_filter: Optional[List[str]] = []
    classname_filter_type: Optional[str] = "in"

class ExtractRequest(BaseModel):
    filter_config: FilterConfig

@app2.post("/extract")
async def extract(
    file: UploadFile = File(...),
    filter_config: str = Form(...)
):
    """
    Extract code from a zip file based on filter configuration.
    """
    # Parse filter config
    print("Filename:", file.filename)

    create_dataset(file.filename)
    try:
        config = FilterConfig(**json.loads(filter_config))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid filter configuration: {str(e)}")
    
    # Save uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    
    try:
        
        temp_file.write(await file.read())
        temp_file.close()
        
        # Process the file
        if file.filename.endswith('.zip'):
            
            results = process_zip(temp_file.name, config)
            
        else:
            
            result = process_file(temp_file.name, config)
            results = [result] if result else []
        
        # Convert to JSONL if requested
        if config.division.get("file", True):
            print(config.division.get("file"))
            #print("output_file",output_file)
            
            return JSONResponse(content={
                "message": "Extraction completed successfully",
                "count": len(results)
            })
        else:
            print("Comes here: ")
            return JSONResponse(content={
                "message": "Extraction completed successfully",
                "count": len(results),
                "results": results
            })
            
    finally:
        # Clean up
        os.unlink(temp_file.name)


@app.route("/")
def home():
    return "Autograder application"

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8000, debug=True)
    uvicorn.run(app2, host="0.0.0.0", port=8080)
