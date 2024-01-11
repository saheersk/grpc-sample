import httpx
from httpx import ConnectError

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from .. import schemas, oauth2, database


router = APIRouter(
    prefix="/task-checker",
    tags=['Tasks Checker']
)

TASK_URL = "http://task-checker:5000/flask"
get_db = database.get_db

@router.get("/gateway/task-checker/")
async def add_task(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{TASK_URL}/')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Microservice 2 error")


@router.get("/gateway/task-checker/all/")
async def get_all_task(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{TASK_URL}/items')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        if isinstance(e, ConnectError):
            raise HTTPException(status_code=503, detail="Service unavailable")
        else:
            raise HTTPException(status_code=e.response.status_code, detail="Microservice 2 error")
        

@router.get("/gateway/task-checker/nats/")
async def get_nats():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{TASK_URL}/nat')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        if isinstance(e, ConnectError):
            raise HTTPException(status_code=503, detail="Service unavailable")
        else:
            raise HTTPException(status_code=e.response.status_code, detail="Microservice 2 error")