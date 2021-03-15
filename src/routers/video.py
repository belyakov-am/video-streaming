import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Request,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from ffmpeg_streaming import (
    Formats,
    Bitrate,
    Representation,
    Size,
    input as ffmpeg_input,
)
from pydantic import BaseModel

from config import VIDEO_DIR, TEMPLATES_DIR


router = APIRouter(
    prefix="/video"
)

templates = Jinja2Templates(directory=TEMPLATES_DIR)


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

    video_dir = VIDEO_DIR / f"{video_uuid}"
    video_dir.mkdir(exist_ok=True)

    # TODO(belyakov): do something with file extension
    video_path = video_dir / "video.mp4"

    # save file to local filesystem
    with open(video_path, "wb+") as f:
        f.write(await file.read())

    # split video into chunks
    video = ffmpeg_input(str(video_path))
    dash = video.dash(Formats.h264())
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    dash.representations(_720p)
    dash.output(str(video_dir / "video.mpd"), async_run=False)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "name": name,
        "uuid": video_uuid,
        "description": description,
    }


@router.get("/stream-v2/{filepath:path}")
async def video_stream_v2(filepath: str):
    return FileResponse(VIDEO_DIR / filepath)


@router.get("/show-v2")
async def video_show_v2(request: Request, video_uuid: str):
    output_dir = VIDEO_DIR / f"{video_uuid}"
    filename = output_dir / "video.mp4"

    # check if file exists
    if not filename.exists():
        # response with not found error
        raise HTTPException(status_code=404, detail="No video with such name")

    details = {
        "path": f"/video/stream-v2/{video_uuid}/video.mpd",
        "type": "video/mp4",
    }

    return templates.TemplateResponse(
        name="video.html",
        context={
            "request": request,
            "details": details,
        }
    )
