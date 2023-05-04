from fastapi import APIRouter, Depends

import menuService.src.crud.menu_item_crud as menu_item_crud
from menuService.src.db.database import SessionLocal, get_db
from menuService.src.schemas.menu_item import MenuItem, MenuItemCreate

router = APIRouter()


@router.get(path="/menu")
def get_menu_items(db=Depends(get_db)) -> list[MenuItem]:
    return menu_item_crud.get_all_items(db)


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
