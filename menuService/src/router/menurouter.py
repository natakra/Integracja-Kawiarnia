from fastapi import APIRouter, Depends

import src.crud.menu_item_crud as menu_item_crud
from src.db.database import SessionLocal, get_db
from src.dependencies import get_ebh
from src.event_bus_handler import EventBusHandler
from src.schemas.menu_item import MenuItem, MenuItemCreate

router = APIRouter()


@router.get(path="/menu")
def get_menu_items(db=Depends(get_db), ebh: EventBusHandler = Depends(get_ebh)) -> list[MenuItem]:
    products_list = menu_item_crud.get_all_items(db)
    ebh.publish_menu_update_event(
        [{"id": product.id, "name": product.name, "price": product.price} for product in products_list])
    return products_list


@router.get(path="/menu/{id}")
def get_menu_items(id: int, db=Depends(get_db)) -> MenuItem:
    return menu_item_crud.get_item(id, db)


@router.post(path="/menu")
async def post_menu_items(
        new_item: MenuItemCreate,
        db: SessionLocal = Depends(get_db)
) -> MenuItem:
    print(new_item)
    return menu_item_crud.add_new_item(new_item, db)


@router.put(path="/menu")
def put_menu_items(new_item: MenuItem, db: SessionLocal = Depends(get_db)) -> None:
    return menu_item_crud.edit_item(new_item, db)
