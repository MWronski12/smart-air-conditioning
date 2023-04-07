from fastapi import APIRouter, HTTPException, status
import requests

BASE_URL = "/api/v1"

router = APIRouter(prefix=BASE_URL)


@router.get("/rooms")
async def rooms_get():
    pass


@router.post("/rooms")
async def rooms_post(room: str) -> str:
    pass

