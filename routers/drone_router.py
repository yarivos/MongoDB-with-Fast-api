from typing import List

from fastapi import APIRouter, Depends
from pymongo.database import Database
from database import get_db

from models.drone import Drone
from config import DRONE_COLLECTION_NAME

drone_api_router = APIRouter(prefix="/drones", tags=["drones"])


@drone_api_router.get("/", response_model=List[Drone])
async def get_drones(db: Database = Depends(get_db)):
    cursor = db[DRONE_COLLECTION_NAME].find()
    # import pdb; pdb.set_trace()
    drones = [Drone(**drone) for drone in cursor]
    return drones


# Endpoint to get a specific drone by ID
@drone_api_router.get("/id/{id}", response_model=Drone)
async def get_drone_by_id(id: int, db: Database = Depends(get_db)):
    # import pdb; pdb.set_trace()
    drone = db[DRONE_COLLECTION_NAME].find_one({"id": id})
    return drone


# Endpoint to get all drones by availability status
@drone_api_router.get("/status/{status}", response_model=List[Drone])
async def get_drones_by_status(status: str, db: Database = Depends(get_db)):
    cursor = db[DRONE_COLLECTION_NAME].find({"status": status})
    drones = [Drone(**drone) for drone in cursor]
    return drones


# Endpoint to update a drone's status
@drone_api_router.put("/{id}")
async def update_drone_status(id: int, status: str, db: Database = Depends(get_db)):
    db[DRONE_COLLECTION_NAME].update_one({"id": id}, {"$set": {"status": status}})


# Endpoint to create a new drone
@drone_api_router.post("/")
async def create_drone(id: int, name: str, status: str, current_mission_id: int, possible_missions_ids,
                       db: Database = Depends(get_db)):
    missions_ids = Drone.transform_possible_missions_ids(possible_missions_ids)
    db[DRONE_COLLECTION_NAME].insert_one(
        {"id": id, "name": name, "status": status, "current_mission_id": current_mission_id,
         "possible_missions_ids": missions_ids})


# Endpoint to modify possible missions for a drone
@drone_api_router.put("/{id}/possible_missions")
async def modify_possible_missions(id: int, possible_missions_ids: str, db: Database = Depends(get_db)):
    missions_ids = Drone.transform_possible_missions_ids(possible_missions_ids)
    db[DRONE_COLLECTION_NAME].update_one({"id": id}, {"$set": {"possible_missions_ids": missions_ids}})
