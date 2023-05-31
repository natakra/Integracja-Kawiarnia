from src.db.database import SessionLocal
from src.db.payment_db import Payments
from src.schemas.payment_schema import CreatePayment


def get_order_by_id(id: int, db: SessionLocal):
    return db.query(Payments).filter(Payments.order_id == id).first()


def post_payment(db: SessionLocal, payment: CreatePayment):
    db_item = Payments(
        order_id=payment.order_id,
        user_id=payment.user_id,
        price=payment.price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
