from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.schemas.response import ApiResponse
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["Clients"])


def find_client(client_id: int, database: Session) -> Client:
    client = ClientService.get_client(database, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
    return client


@router.get("", response_model=ApiResponse[list[ClientRead]])
def get_clients(database: Session = Depends(get_db)) -> ApiResponse[list[ClientRead]]:
    return ApiResponse(message="Clients retrieved successfully.", data=ClientService.list_clients(database))


@router.get("/{client_id}", response_model=ApiResponse[ClientRead])
def get_client(client_id: int, database: Session = Depends(get_db)) -> ApiResponse[ClientRead]:
    return ApiResponse(message="Client retrieved successfully.", data=find_client(client_id, database))


@router.post("", response_model=ApiResponse[ClientRead], status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, database: Session = Depends(get_db)) -> ApiResponse[ClientRead]:
    try:
        client = ClientService.create_client(database, payload)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return ApiResponse(message="Client created successfully.", data=client)


@router.put("/{client_id}", response_model=ApiResponse[ClientRead])
def update_client(client_id: int, payload: ClientUpdate, database: Session = Depends(get_db)) -> ApiResponse[ClientRead]:
    client = find_client(client_id, database)
    try:
        updated_client = ClientService.update_client(database, client, payload)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return ApiResponse(message="Client updated successfully.", data=updated_client)


@router.delete("/{client_id}", response_model=ApiResponse[None])
def delete_client(client_id: int, database: Session = Depends(get_db)) -> ApiResponse[None]:
    ClientService.delete_client(database, find_client(client_id, database))
    return ApiResponse(message="Client deleted successfully.")
