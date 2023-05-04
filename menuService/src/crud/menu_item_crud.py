from menuService.src.db.database import SessionLocal
from menuService.src.db.menu_item_db import MenuItem as MenuItemDb
from menuService.src.schemas.menu_item import MenuItemCreate, MenuItem


def get_all_items(db: SessionLocal):
    return db.query(MenuItemDb).offset(0).all()


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