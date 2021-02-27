import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
)
from fastapi.responses import StreamingResponse

from src.config import VIDEO_DIR
from src.utils import video_frames_generator


router = APIRouter(
    prefix="/video"
)


@router.post("/upload")
# TODO(belyakov): get more metadata and save it to db
async def video_upload(name: str, description: str, file: UploadFile = File(...)):
    # TODO(belyakov): check filename for . and /

    video_uuid = uuid.uuid4()
    # TODO(belyakov): to something with file extension
    video_path = VIDEO_DIR + str(video_uuid) + ".mp4"

    # save file to local filesystem
    with open(video_path, "wb+") as f:
        f.write(await file.read())

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "name": name,
        "description": description,
    }


@router.get("/stream")
async def video_stream(name: str):
    # TODO(belyakov): accept more metadata and get uuid from db
    filename = VIDEO_DIR + name + ".mp4"

    # check if file exists
    try:
        f = open(filename)
    except IOError:
        # response with not found error
        raise HTTPException(status_code=404, detail="No video with such name")

    return StreamingResponse(
        content=video_frames_generator(filename),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
