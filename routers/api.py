from routers.drone_router import drone_api_router
from routers.mission_router import mission_api_router
from routers.schedule_router import schedule_api_router
from routers.trajectory_router import trajectory_api_router
from fastapi import APIRouter

router = APIRouter()


def include_all_routers():
    router.include_router(drone_api_router)
    router.include_router(mission_api_router)
    router.include_router(schedule_api_router)
    router.include_router(trajectory_api_router)


include_all_routers()
