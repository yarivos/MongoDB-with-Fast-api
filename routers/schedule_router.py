from datetime import datetime, timedelta
from http.client import HTTPException
from typing import List, Literal
from fastapi import APIRouter, Depends
from pymongo.database import Database, Collection
import threading
from database import get_db

from models.schedule import Schedule
from config import SCHEDULE_COLLECTION_NAME, DRONE_COLLECTION_NAME
from routers.drone_router import update_drone_status, get_drone_by_id

# from email_notifier import GeneralNotifier, ExceptionNotifier

schedule_api_router = APIRouter(prefix="/schedules", tags=["schedules"])


def check_existing_schedule(collection: Collection, drone_id: int,
                            start_time: datetime, end_time: datetime) -> bool:
    """
    Check if there's an existing schedule for a drone that overlaps with the given time range.

    Parameters:
        collection (Collection): MongoDB collection object.
        drone_id (int): ID of the drone.
        start_time (datetime): Start time of the new schedule.
        end_time (datetime): End time of the new schedule.

    Returns:
        bool: True if there's an existing schedule that overlaps; False otherwise.
    """
    existing_schedule = collection.find_one({
        "drone_id": drone_id,
        "start_time": {"$lt": end_time},
        "end_time": {"$gt": start_time}
    })
    return True if existing_schedule else None


def start_mission_change_status(schedule_id: int, drone_id: int

                                , mission_id: int, start_time: datetime, end_time: datetime) -> None:
    """
     Schedule a mission to change the status of the drone and the schedule when it starts.

     Parameters:
         schedule_id (int): ID of the schedule.
         drone_id (int): ID of the drone.
         mission_id (int): ID of the mission.
         start_time (datetime): Start time of the mission.
         end_time (datetime): End time of the mission.

     Returns:
         None
     """
    time_until_start = (start_time - datetime.now()).total_seconds()
    threading.Timer(time_until_start, change_drone_status, [drone_id, "on-mission"])
    threading.Timer(time_until_start, update_schedule_status, [schedule_id, "in-progress"])
    threading.Timer(time_until_start, mission_start_notifier, [drone_id, mission_id, end_time - start_time])


# function is built to send notifications to any interface.
# message: drone: {drone_id} is starting mission: {mission_id}. approximate finishing time: {mission_time}
def mission_start_notifier(drone_id: int, mission_id: int, mission_time: timedelta):
    pass


def end_mission_change_status(schedule_id: int, drone_id: int, end_time: datetime) -> None:
    """
      Schedule a mission to change the status of the drone and the schedule when it ends.

      Parameters:
          schedule_id (int): ID of the schedule.
          drone_id (int): ID of the drone.
          end_time (datetime): End time of the mission.

      Returns:
          None
      """
    time_until_end = (end_time - datetime.now()).total_seconds()
    threading.Timer(time_until_end, change_drone_status, [drone_id, "available"])
    threading.Timer(time_until_end, update_schedule_status, [schedule_id, "completed"])


def change_drone_status(drone_id: id, status: Literal['available', 'on-mission', 'pending']) -> None:
    """
      Change the status of a drone.

      Parameters:
          drone_id (id): ID of the drone.
          status (Literal['available', 'on-mission', 'pending']): New status of the drone.

      Returns:
          None
      """
    update_drone_status(drone_id, status)


# Endpoint to create a new mission
@schedule_api_router.post("/")
async def create_schedule(id: int, drone_id: int, mission_id: int,
                          start_time: str, end_time: str, status: str,
                          db: Database = Depends(get_db)):
    if (get_drone_by_id(drone_id) is None):
        raise HTTPException(status_code=400, detail="Drone doesn't exist")
    mod_start_time: datetime = Schedule.transform_time(start_time)
    mod_end_time: datetime = Schedule.transform_time(end_time)

    # check if drone is already booked
    if not check_existing_schedule(drone_id, mod_start_time, mod_end_time):
        start_mission_change_status(id, drone_id, mission_id, start_time, end_time)
        end_mission_change_status(id, drone_id, end_time)
        db[SCHEDULE_COLLECTION_NAME].insert_one(
            {"id": id, "drone_id": drone_id, "mission_id": mission_id, "start_time": mod_start_time,
             "end_time": mod_end_time,
             "status": status})
        return
    raise HTTPException(status_code=400, detail="Drone already booked for overlapping schedule")


@schedule_api_router.get("/", response_model=list[Schedule])
async def get_schedules(db: Database = Depends(get_db)):
    cursor = db[SCHEDULE_COLLECTION_NAME].find()
    schedules = [Schedule(**schedule) for schedule in cursor]
    return schedules


# Endpoint to update a schedule's status
@schedule_api_router.put("/{id}")
async def update_schedule_status(id: int, status: str, db: Database = Depends(get_db)):
    db[SCHEDULE_COLLECTION_NAME].update_one({"id": id}, {"$set": {"status": status}})


# Endpoint to get schedules date range
@schedule_api_router.get("/{start_date}/{end_date}", response_model=List[Schedule])
async def get_schedules_date_range(start_date: str, end_date: str, db: Database = Depends(get_db)):
    tr_start_date: datetime = Schedule.transform_time(start_date)
    tr_end_date: datetime = Schedule.transform_time(end_date)
    cursor = db[SCHEDULE_COLLECTION_NAME].find({
        "$and": [
            {"start_time": {"$gte": tr_start_date}},
            {"end_time": {"$lte": tr_end_date}},
        ]
    }
    )
    schedules = [Schedule(**schedule) for schedule in cursor]
    return schedules


# Endpoint to get schedules by drone
@schedule_api_router.get("/{drone_id}", response_model=List[Schedule])
async def get_schedules_by_drone(drone_id: int, db: Database = Depends(get_db)):
    cursor = db[SCHEDULE_COLLECTION_NAME].find({"drone_id": drone_id})
    schedules = [Schedule(**schedule) for schedule in cursor]
    return schedules
