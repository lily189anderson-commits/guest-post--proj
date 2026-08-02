from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.order import Order, LinkStatus, PaymentStatus
from app.domain.repositories.interfaces import OrderRepository
from app.infrastructure.database.models import OrderModel


def _to_entity(row: OrderModel) -> Order:
    return Order(
        id=row.id, client_id=row.client_id, website_id=row.website_id,
        target_link=row.target_link, anchor_text=row.anchor_text, price=row.price,
        paid_amount=row.paid_amount, payment_status=PaymentStatus(row.payment_status),
        link_status=LinkStatus(row.link_status), last_checked_at=row.last_checked_at,
        created_at=row.created_at,
    )


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, db: Session):
        self._db = db

    def create(self, order: Order) -> Order:
        row = OrderModel(
            client_id=order.client_id, website_id=order.website_id,
            target_link=order.target_link, anchor_text=order.anchor_text,
            price=order.price, paid_amount=order.paid_amount,
            payment_status=order.payment_status.value, link_status=order.link_status.value,
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return _to_entity(row)

    def get_by_id(self, order_id: int) -> Optional[Order]:
        row = self._db.query(OrderModel).filter(OrderModel.id == order_id).first()
        return _to_entity(row) if row else None

    def list_all(self) -> List[Order]:
        return [_to_entity(r) for r in self._db.query(OrderModel).order_by(OrderModel.id.desc()).all()]

    def update(self, order: Order) -> Order:
        row = self._db.query(OrderModel).filter(OrderModel.id == order.id).first()
        if row is None:
            raise LookupError(f"Order {order.id} not found")
        row.target_link = order.target_link
        row.anchor_text = order.anchor_text
        row.price = order.price
        row.paid_amount = order.paid_amount
        row.payment_status = order.payment_status.value
        row.link_status = order.link_status.value
        row.last_checked_at = order.last_checked_at
        self._db.commit()
        self._db.refresh(row)
        return _to_entity(row)

    def delete(self, order_id: int) -> bool:
        row = self._db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if row is None:
            return False
        self._db.delete(row)
        self._db.commit()
        return True
