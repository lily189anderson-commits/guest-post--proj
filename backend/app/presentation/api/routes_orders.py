from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.order_service import OrderService
from app.presentation.api.deps import get_order_service, get_current_username
from app.presentation.schemas.order_schema import OrderCreateRequest, PaymentRequest, OrderResponse

router = APIRouter(prefix="/api/orders", tags=["Orders"], dependencies=[Depends(get_current_username)])


def _to_response(order) -> OrderResponse:
    return OrderResponse(
        id=order.id, client_id=order.client_id, website_id=order.website_id,
        target_link=order.target_link, anchor_text=order.anchor_text, price=order.price,
        paid_amount=order.paid_amount, pending_amount=order.pending_amount,
        payment_status=order.payment_status.value, link_status=order.link_status.value,
        last_checked_at=order.last_checked_at, created_at=order.created_at,
    )


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreateRequest, service: OrderService = Depends(get_order_service)):
    try:
        order = service.create_order(payload.client_id, payload.website_id, payload.target_link,
                                      payload.anchor_text, payload.price)
        return _to_response(order)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[OrderResponse])
def list_orders(service: OrderService = Depends(get_order_service)):
    return [_to_response(o) for o in service.list_orders()]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, service: OrderService = Depends(get_order_service)):
    order = service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return _to_response(order)


@router.post("/{order_id}/payments", response_model=OrderResponse)
def record_payment(order_id: int, payload: PaymentRequest, service: OrderService = Depends(get_order_service)):
    try:
        order = service.record_payment(order_id, payload.amount)
        return _to_response(order)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, service: OrderService = Depends(get_order_service)):
    if not service.delete_order(order_id):
        raise HTTPException(status_code=404, detail="Order not found")
