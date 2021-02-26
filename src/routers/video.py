from fastapi import APIRouter


router = APIRouter(
    prefix="/video"
)


@router.get("/")
async def root():
    return {"message": "Hello World"}
