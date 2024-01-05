import httpx

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import logging

logger = logging.getLogger(__name__)

from .. import schemas, oauth2, database


router = APIRouter(
    prefix="/gateway",
    tags=['Tasks']
)

get_db = database.get_db

TASK_URL = "http://task-app:8000/task/api/v1/service/"


async def process_task_request(method: str, data: schemas.Task = None):
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Attempting to connect to: {TASK_URL}")
            if method == "GET":
                response = await client.get(TASK_URL)
            elif method == "POST":
                encoded_data = jsonable_encoder(data)
                response = await client.post(TASK_URL, json=encoded_data)
            else:
                raise HTTPException(status_code=405, detail="Method Not Allowed")

            response.raise_for_status()
            return response.json()
        
    except httpx.ConnectError as ce:
        logger.error(f"ConnectError: {ce}")
        print(f"ConnectError: {ce}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Microservice 1 error")

@router.get("/task/")
async def gateway_task_get():
    return await process_task_request("GET")

@router.post("/task/")
async def gateway_task_post(data: schemas.Task, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await process_task_request("POST", data)
    

async def process_task_detail_request(method: str, id: int, data: schemas.Task = None):
    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(f"{TASK_URL}{id}/")
            elif method == "PUT":
                encoded_data = jsonable_encoder(data)
                response = await client.put(f"{TASK_URL}{id}/", json=encoded_data)
            elif method == "DELETE":
                response = await client.delete(f"{TASK_URL}{id}/")
            else:
                raise HTTPException(status_code=405, detail="Method Not Allowed")

            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Microservice 1 error")

@router.get("/task/{id}/")
async def gateway_task_detail(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await process_task_detail_request("GET", id)

@router.put("/task/{id}/")
async def gateway_task_update(id: int, data: schemas.Task, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await process_task_detail_request("PUT", id, data)

@router.delete("/task/{id}/")
async def gateway_task_delete(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await process_task_detail_request("DELETE", id)
