from typing import List

from src.db.database import SessionLocal
from src.db.menu_item_db import MenuItem as MenuItemsDb
from src.db.order_db import Order as OrderDb
from src.schemas.order_schemas import CreateOrder, OrderStatus


def get_menu_item_by_id(db: SessionLocal, product_id):
    return db.query(MenuItemsDb).filter(MenuItemsDb.id == product_id).first()


def update_menu(db: SessionLocal, menu_dict_list):
    db.query(MenuItemsDb).delete()
    for item in menu_dict_list:
        db_item = MenuItemsDb(
            id=item["id"],
            price=item["price"]
        )
        db.add(db_item)
    db.commit()
    return db.query(MenuItemsDb).offset(0).all()


def calculate_price(db: SessionLocal, product_ids: List[int]):
    price = 0
    for product_id in product_ids:
        price += get_menu_item_by_id(db, product_id).price
    return price


def create_order(db: SessionLocal, order_form: CreateOrder, user_id):
    price = calculate_price(db, order_form.product_ids)
    db_item = OrderDb(
        user_id=user_id,
        price=price,
        status=OrderStatus.STATUS_ACCEPTED.value
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def order_status_update(db: SessionLocal, id: int, status: str):
    db.query(OrderDb).filter(OrderDb.id == id).update({
        "status": status
    })
    db.commit()
    return db.query(OrderDb).filter(OrderDb.id == id).first()


def get_orders(db: SessionLocal):
    return db.query(OrderDb).offset(0).all()


def get_order_by_id(id: int, db: SessionLocal):
    return db.query(OrderDb).filter(OrderDb.id == id).first()


def get_orders_by_user_id(user_id: str, db: SessionLocal):
    return db.query(OrderDb).filter(OrderDb.user_id == user_id).offset(0).all()
