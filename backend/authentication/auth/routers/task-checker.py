import httpx

from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/task-checker",
    tags=['Tasks Checker']
)

TASK_URL = "http://localhost:8003/"


@router.get("/")
async def microservice1():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(TASK_URL)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Microservice 1 error")

@router.get("/")
async def microservice2():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(TASK_URL)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Microservice 2 error")