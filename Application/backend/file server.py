from fastapi import APIRouter, Depends, HTTPException, status
router = APIRouter(tags=['File Management'])

# upload files from fastapi
from fastapi import FastAPI, UploadFile, File
app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(file.filename, 'wb') as image:
        content = await file.read()
        image.write(content)
        image.close()
    return JSONResponse(content={"filename": file.filename},
status_code=200)


# download files using FastAPI
from fastapi import FastAPI
from os import getcwd
from fastapi.responses import FileResponse
app = FastAPI()

@router.get("/download/{name_file}")
def download_file(name_file: str):
    return FileResponse(path=getcwd() + "/" + name_file, media_type='application/octet-stream', filename=name_file)


# get files using fastapi
from fastapi import FastAPI
from os import getcwd
from fastapi.responses import FileResponse

app = FastAPI()

@router.get("/file/{name_file}")
def get_file(name_file: str):
    return FileResponse(path=getcwd() + "/" + name_file)


# delete files using fastapi
from fastapi import FastAPI
from os import getcwd, remove
from fastapi.responses import JSONResponse

app = FastAPI()

@router.delete("/delete/file/{name_file}")
def delete_file(name_file: str):
    try:
        remove(getcwd() + "/" + name_file)
        return JSONResponse(content={
            "removed": True
            }, status_code=200)   
    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "error_message": "File not found"
        }, status_code=404)