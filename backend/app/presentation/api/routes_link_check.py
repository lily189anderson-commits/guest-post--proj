from fastapi import APIRouter, Depends, HTTPException

from app.application.services.link_checker_service import LinkCheckerService
from app.presentation.api.deps import get_link_checker_service, get_current_username
from app.presentation.schemas.order_schema import LinkCheckRequest, BulkLinkCheckRequest, OrderResponse

router = APIRouter(prefix="/api/link-check", tags=["Link Health Checker"],
                    dependencies=[Depends(get_current_username)])


def _to_response(order) -> OrderResponse:
    return OrderResponse(
        id=order.id, client_id=order.client_id, website_id=order.website_id,
        target_link=order.target_link, anchor_text=order.anchor_text, price=order.price,
        paid_amount=order.paid_amount, pending_amount=order.pending_amount,
        payment_status=order.payment_status.value, link_status=order.link_status.value,
        last_checked_at=order.last_checked_at, created_at=order.created_at,
    )


@router.post("/{order_id}", response_model=OrderResponse)
def check_single_order(order_id: int, payload: LinkCheckRequest,
                        service: LinkCheckerService = Depends(get_link_checker_service)):
    """Check whether a single order's backlink is live on the given page URL."""
    try:
        order = service.check_order(order_id, payload.page_url)
        return _to_response(order)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/bulk", response_model=list[OrderResponse])
def check_all_orders(payload: BulkLinkCheckRequest,
                      service: LinkCheckerService = Depends(get_link_checker_service)):
    """
    Bulk-check every order that has a page URL supplied.
    Body: {"page_urls": {"1": "https://blog.com/post-1", "2": "https://blog.com/post-2"}}
    """
    page_urls = {int(k): v for k, v in payload.page_urls.items()}
    results = service.check_all(page_urls)
    return [_to_response(o) for o in results]
