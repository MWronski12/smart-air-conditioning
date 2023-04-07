from fastapi import APIRouter, HTTPException, status

BASE_URL = "/api/v1"

router = APIRouter(prefix=BASE_URL)

@router.post()