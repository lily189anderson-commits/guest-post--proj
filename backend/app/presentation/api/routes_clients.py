from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.client_service import ClientService
from app.presentation.api.deps import get_client_service, get_current_username
from app.presentation.schemas.client_schema import ClientCreateRequest, ClientUpdateRequest, ClientResponse

router = APIRouter(prefix="/api/clients", tags=["Clients"], dependencies=[Depends(get_current_username)])


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreateRequest, service: ClientService = Depends(get_client_service)):
    try:
        client = service.create_client(payload.name, payload.email, payload.phone, payload.notes)
        return ClientResponse.model_validate(client, from_attributes=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[ClientResponse])
def list_clients(service: ClientService = Depends(get_client_service)):
    return [ClientResponse.model_validate(c, from_attributes=True) for c in service.list_clients()]


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, service: ClientService = Depends(get_client_service)):
    client = service.get_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return ClientResponse.model_validate(client, from_attributes=True)


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, payload: ClientUpdateRequest, service: ClientService = Depends(get_client_service)):
    try:
        client = service.update_client(client_id, payload.name, payload.email, payload.phone, payload.notes)
        return ClientResponse.model_validate(client, from_attributes=True)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, service: ClientService = Depends(get_client_service)):
    if not service.delete_client(client_id):
        raise HTTPException(status_code=404, detail="Client not found")
