from fastapi import (
    Request,
)
from fastapi.templating import Jinja2Templates

from config import TEMPLATES_DIR


templates = Jinja2Templates(directory=TEMPLATES_DIR)


async def root(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse(
        name="root.html",
        context={
            "request": request,
        }
    )
