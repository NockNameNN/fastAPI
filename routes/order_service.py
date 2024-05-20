from fastapi import APIRouter


router = APIRouter(
    prefix="/order-service",
    tags=["Услуга заказа"]
)

@router.get("/")
async def get_order_service() -> int:
    return 5