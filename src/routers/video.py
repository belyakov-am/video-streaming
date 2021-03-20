import uuid
import os

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
async def video_upload(
        request: Request,
        name: str,
        description: str,
        file: UploadFile = File(...),
):
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

    # upload video info to db
    await request.app.db.insert_video_info(
        video_uuid=video_uuid,
        name=name,
        description=description
    )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "name": name,
        "uuid": video_uuid,
        "description": description,
    }


@router.get("/stream/{filepath:path}", include_in_schema=False)
async def video_stream(filepath: str):
    print(VIDEO_DIR / filepath)
    return FileResponse(VIDEO_DIR / filepath)


@router.get("/show")
async def video_show(request: Request, video_uuid: str):
    video_uuids = os.listdir(VIDEO_DIR)

    output_dir = VIDEO_DIR / f"{video_uuid}"
    filename = output_dir / "video.mp4"

    # check if file exists
    if not filename.exists():
        # response with not found error
        raise HTTPException(status_code=404, detail="No video with such name")


    films = []
    for video_uuid in video_uuids:
        film = {}
        film['path'] = f"/video/stream/{video_uuid}/video.mpd"
        film['name'] = f"Name-{video_uuid}"
        film['description'] = f"This is description of the film {video_uuid}"
        films.append(film)

    print(films, flush=True)
    details = {
        "films": films,
        "type": "video/mp4",
    }

    return templates.TemplateResponse(
        name="video.html",
        context={
            "request": request,
            "details": details,
        }
    )
