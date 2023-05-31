from src.db.database import SessionLocal
from src.db.menu_item_db import MenuItem as MenuItemDb
from src.schemas.menu_item import MenuItemCreate, MenuItem


def fake_menu(db: SessionLocal):
    add_new_item(MenuItemCreate(
        name="Frytki",
        price=8.9
    ), db)
    add_new_item(MenuItemCreate(
        name="Kawa",
        price=10
    ), db)
    add_new_item(MenuItemCreate(
        name="Pączek",
        price=5
    ), db)
    add_new_item(MenuItemCreate(
        name="Cola",
        price=13
    ), db)
    add_new_item(MenuItemCreate(
        name="Ciastko",
        price=6
    ), db)


def get_all_items(db: SessionLocal):
    menu_items = db.query(MenuItemDb).offset(0).all()
    if len(menu_items) == 0:
        fake_menu(db)
        menu_items = db.query(MenuItemDb).offset(0).all()
    return menu_items


def add_new_item(new_item: MenuItemCreate, db: SessionLocal):
    db_item = MenuItemDb(name=new_item.name, price=new_item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def edit_item(new_item: MenuItem, db):
    db.query(MenuItemDb).filter(MenuItemDb.id == new_item.id).update({
        "name": new_item.name,
        "price": new_item.price
    })
    db.commit()
    return db.query(MenuItemDb).filter(MenuItemDb.id == new_item.id).first()


def get_item(id: int, db: SessionLocal):
    return db.query(MenuItemDb).filter(MenuItemDb.id == id).first()
