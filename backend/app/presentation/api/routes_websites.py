from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.website_service import WebsiteService
from app.presentation.api.deps import get_website_service, get_current_username
from app.presentation.schemas.website_schema import (
    WebsiteCreateRequest, WebsiteMetricsUpdateRequest, WebsiteResponse,
)

router = APIRouter(prefix="/api/websites", tags=["Websites"], dependencies=[Depends(get_current_username)])


@router.post("", response_model=WebsiteResponse, status_code=status.HTTP_201_CREATED)
def create_website(payload: WebsiteCreateRequest, service: WebsiteService = Depends(get_website_service)):
    try:
        website = service.create_website(payload.domain, payload.da_score, payload.dr_score,
                                           payload.niche, payload.notes)
        return WebsiteResponse.model_validate(website, from_attributes=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[WebsiteResponse])
def list_websites(service: WebsiteService = Depends(get_website_service)):
    return [WebsiteResponse.model_validate(w, from_attributes=True) for w in service.list_websites()]


@router.get("/{website_id}", response_model=WebsiteResponse)
def get_website(website_id: int, service: WebsiteService = Depends(get_website_service)):
    website = service.get_website(website_id)
    if website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    return WebsiteResponse.model_validate(website, from_attributes=True)


@router.put("/{website_id}/metrics", response_model=WebsiteResponse)
def update_metrics(website_id: int, payload: WebsiteMetricsUpdateRequest,
                    service: WebsiteService = Depends(get_website_service)):
    try:
        website = service.update_metrics(website_id, payload.da_score, payload.dr_score)
        return WebsiteResponse.model_validate(website, from_attributes=True)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{website_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_website(website_id: int, service: WebsiteService = Depends(get_website_service)):
    if not service.delete_website(website_id):
        raise HTTPException(status_code=404, detail="Website not found")
