import uuid

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from src.config import VIDEO_DIR


router = APIRouter(
    prefix="/video"
)


@router.post("/upload")
async def video_upload(name: str, description: str, file: UploadFile = File(...)):
    # TODO(belyakov): check filename for . and /

    video_uuid = uuid.uuid4()
    # TODO(belyakov): to something with file extension
    video_path = VIDEO_DIR + str(video_uuid) + ".mp4"

    with open(video_path, "wb+") as f:
        f.write(await file.read())

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "name": name,
        "description": description,
    }

