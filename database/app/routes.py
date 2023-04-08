from fastapi import APIRouter, HTTPException, status
import requests

BASE_URL = "/api/v1"

router = APIRouter(prefix=BASE_URL)
