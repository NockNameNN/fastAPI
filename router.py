from routes import brand, car, customer_car, order, order_service, role, role_user, service, user

from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1",
)


router.include_router(brand.router)
router.include_router(car.router)
router.include_router(customer_car.router)
router.include_router(order.router)
router.include_router(order_service.router)
router.include_router(role.router)
router.include_router(role_user.router)
router.include_router(service.router)
router.include_router(user.router)
