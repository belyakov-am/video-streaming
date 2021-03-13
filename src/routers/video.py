import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Request,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel

from config import VIDEO_DIR
from utils import video_frames_generator


router = APIRouter(
    prefix="/video"
)

templates = Jinja2Templates(directory="templates")


class VideoUploadResponse(BaseModel):
    filename: str
    content_type: str
    name: str
    uuid: str
    description: str


@router.post("/upload", response_model=VideoUploadResponse)
# TODO(belyakov): get more metadata and save it to db
async def video_upload(name: str, description: str, file: UploadFile = File(...)):
    # TODO(belyakov): check filename for . and /

    video_uuid = str(uuid.uuid4())
    # TODO(belyakov): do something with file extension
    video_path = VIDEO_DIR + video_uuid + ".mp4"

    # save file to local filesystem
    with open(video_path, "wb+") as f:
        f.write(await file.read())

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "name": name,
        "uuid": video_uuid,
        "description": description,
    }


@router.get(
    path="/stream",
    responses={
        200: {
            "content": {"multipart/x-mixed-replace": {}},
            "description": "Return video as a stream of jpeg frames",
        },
        404: {
            "description": "No video with such name",
        },
    }
)
async def video_stream(video_uuid: str):
    # TODO(belyakov): accept more metadata and get uuid from db
    filename = VIDEO_DIR + video_uuid + ".mp4"

    # check if file exists
    try:
        open(filename)
    except IOError:
        # response with not found error
        raise HTTPException(status_code=404, detail="No video with such name")

    return StreamingResponse(
        content=video_frames_generator(filename),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.get("/show", response_class=HTMLResponse)
async def video_show(request: Request, video_uuid: str):
    return templates.TemplateResponse(
        name="base.html",
        context={
            "request": request,
            "video_uuid": video_uuid,
        }
    )
