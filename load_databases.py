from typing import Dict
from pydantic import BaseModel
from pymongo.database import Database
from config import COLLECTION_SOURCES
from models.drone import Drone
from models.mission import Mission
from models.schedule import Schedule
from models.trajectory import Trajectory
import pandas as pd

collection_name_to_model: Dict[str, BaseModel] = {
    "drones": Drone,
    "missions": Mission,
    "schedules": Schedule,
    "trajectories": Trajectory,
}
"""
Dictionary mapping collection names to Pydantic BaseModel classes representing the respective MongoDB collections.
"""

def load_databases(database: Database):
    """
    Load data from CSV files into collections.

    Parameters:
        database (Database): MongoDB database object.

    Returns:
        None
    """
    for collection_source in COLLECTION_SOURCES:
        collection = collection_source.lower().replace("db", "")
        df = pd.read_csv(f"databases/{collection_source}.csv")
        database[collection].drop()
        for index in df.index:
            model = collection_name_to_model[collection](**df.loc[index].to_dict())
            database[collection].insert_one(model.dict())
