from fastapi import APIRouter, Depends
from pymongo.database import Database
from database import get_db

from models.mission import Mission
from config import MISSION_COLLECTION_NAME

mission_api_router = APIRouter(prefix="/missions", tags=["missions"])


@mission_api_router.get("/", response_model=list[Mission])
async def get_missions(db: Database = Depends(get_db)):
    cursor = db[MISSION_COLLECTION_NAME].find()
    missions = [Mission(**mission) for mission in cursor]
    return missions


# Endpoint to create a new mission
@mission_api_router.post("/")
async def create_mission(id: int, trajectory: str, duration: int, priority: int,
                         db: Database = Depends(get_db)):
    db[MISSION_COLLECTION_NAME].insert_one(
        {"id": id, "trajectory": trajectory, "duration": duration, "priority": priority, })


# Endpoint to get all drones by availability status
@mission_api_router.get("/{trajectory_id}", response_model=list[Mission])
async def get_missions_by_trajectory_id(trajectory_id: int, db: Database = Depends(get_db)):
    cursor = db[MISSION_COLLECTION_NAME].find({"trajectory_id": trajectory_id})
    missions = [Mission(**mission) for mission in cursor]
    return missions


# Endpoint to get a specific drone by ID
@mission_api_router.get("/{id}", response_model=Mission)
async def get_mission_by_id(id: int, db: Database = Depends(get_db)):
    mission = db.MISSION_COLLECTION_NAME.find_one({"id": id})
    return mission
