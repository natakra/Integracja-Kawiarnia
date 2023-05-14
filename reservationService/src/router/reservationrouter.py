from fastapi import APIRouter, Path

router = APIRouter()


@router.get("/tables/{table_id}")
def get_available_tables(table_id: str = Path()):
    return {
        "table_id": table_id,
        "availability": True
    }
