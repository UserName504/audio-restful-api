from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse, Response, JSONResponse
from pathlib import Path
from typing import List
from pydub import AudioSegment
from starlette.responses import StreamingResponse
from datetime import datetime
import json
from dbfs import adjust_volume

app = FastAPI()

@app.post('/adjust_volume')
async def adjust_volume_api(request: Request):
    try:
        data = await request.json()
        input_file = data.get('input_file')
        output_file = data.get('output_file')
        target_dBFS = data.get('target_dBFS')
        if not input_file or not output_file or target_dBFS is None:
            raise HTTPException(status_code=400, detail='Invalid input')
        # Check if the file has a valid audio extension
        valid_audio_formats = ["wav", "mp3", "ogg", "flac", "aac", "m4a"]
        file_extension = input_file.split('.')[-1].lower()
        if file_extension not in valid_audio_formats:
            raise HTTPException(status_code=400, detail='Not a valid audio file')
        adjust_volume(input_file, output_file, target_dBFS)
        return JSONResponse(content={'success': True})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Incorrect file type.' + str(e))

@app.get("/test/")
async def the_test():
    return {"key": "value", "message": "hello world" }

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file in the "uploads" directory
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(parents=True, exist_ok=True)
        file_path = uploads_dir / file.filename

        with file_path.open("wb") as f:
            f.write(file.file.read())

        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/downloadfile/{filename}")
async def read_upload_file(filename: str):
    try:
        # Return the requested file for download
        file_path = Path("uploads") / filename
        if file_path.exists():
            return FileResponse(file_path, filename=filename)
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/listfiles/")
async def list_files():
    try:
        # List all files in the "uploads" directory
        uploads_dir = Path("uploads")
        file_list = [str(file.name) for file in uploads_dir.iterdir() if file.is_file()]
        return {"files": file_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/deletefile/{filename}")
async def delete_file(filename: str):
    try:
        # Delete the specified file from the "uploads" directory
        file_path = Path("uploads") / filename
        if file_path.exists():
            file_path.unlink()
            return {"message": f"File '{filename}' has been deleted!"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#
# Function to get the OpenAPI schema
def get_openapi_schema():
    return get_openapi(
        title="Audio Restful APIYour API Title",
        version="3.1.0",
        description="An API to upload, download, and alter the dBFS of audio files.",
        routes=app.routes,
    )

# Save the OpenAPI schema to a file
def save_openapi_schema():
    openapi_schema = get_openapi_schema()
    file_path = Path("openapi.json")
    with file_path.open("w") as file:
        json.dump(openapi_schema, file, indent=2)
#
if __name__ == '__main__':
    import uvicorn

    # Save the OpenAPI schema before running the application
    save_openapi_schema()

    uvicorn.run(app, host='127.0.0.1', port=8000)