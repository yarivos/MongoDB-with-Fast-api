from fastapi import APIRouter, Depends
from pymongo.database import Database
from database import get_db

from models.trajectory import Trajectory
from config import TRAJECTORY_COLLECTION_NAME

trajectory_api_router = APIRouter(prefix="/trajectories", tags=["trajectories"])

# Endpoint to create a new trajectory
@trajectory_api_router.post("/")
async def create_trajectory(id: int, description: str, type: str, number_of_products: int,
                            db: Database = Depends(get_db)):
    db[TRAJECTORY_COLLECTION_NAME].insert_one(
        {"id": id, "description": description, "type": type, "number_of_products": number_of_products, })

# Endpoint to get a specific trajectory by ID
@trajectory_api_router.get("/{id}", response_model=Trajectory)
async def get_trajectory_by_id(id: int, db: Database = Depends(get_db)):
    return db[TRAJECTORY_COLLECTION_NAME].find_one({"id": id})
