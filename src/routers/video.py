import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Request,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config import TEMPLATES_DIR
from src.routers.upload import upload_file


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
    # TODO(belyakov): do something with file extension

    video_uuid = str(uuid.uuid4())

    # upload video to storage
    storage_video_uid = await upload_file(file.file)
    if storage_video_uid is None:
        print('[ERROR] upload failed')
    else:
        print("[INFO] uploaded file as:", storage_video_uid)

    # upload video info to db
    await request.app.db.insert_video_info(
        video_uuid=video_uuid,
        name=name,
        storage_video_uid=storage_video_uid,
        description=description
    )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "name": name,
        "uuid": video_uuid,
        "description": description,
        "storage_video_uid": storage_video_uid,
    }


@router.get("/show")
async def video_show(request: Request):
    videos_info = await request.app.db.select_video_info()
    videos = []
    for video_info in videos_info:
        video = {
            "uid": video_info["storage_video_uid"],
            "name": video_info["name"],
            "description": video_info["description"],
        }
        videos.append(video)

    details = {
        "films": videos,
        "type": "video/mp4",
    }

    return templates.TemplateResponse(
        name="video.html",
        context={
            "request": request,
            "details": details,
        }
    )
