from datetime import datetime
from typing import Union, Literal
from pydantic import BaseModel, validator


class Schedule(BaseModel):
    """
    Represents a schedule object with attributes including its ID, drone ID,
    mission ID, start time, end time, and status.
    """

    id: int
    """Unique identifier for the schedule."""

    drone_id: int
    """ID of the drone associated with the schedule."""

    mission_id: int
    """ID of the mission associated with the schedule."""

    start_time: datetime
    """Start time of the schedule."""

    end_time: datetime
    """End time of the schedule."""

    status: Literal['in-progress', 'scheduled', 'completed', 'pending']
    """
    Status of the schedule. It can be one of the following:
    - 'in-progress': Schedule is currently in progress.
    - 'scheduled': Schedule is scheduled for execution.
    - 'completed': Schedule has been completed.
    - 'pending': Schedule is pending for execution.
    """

    @classmethod
    def transform_time(cls, raw_value: Union[str, datetime]) -> datetime:
        """
        Class method to transform raw time data into a datetime object.

        Parameters:
            raw_value (Union[str, datetime]): Raw value representing time data.

        Returns:
            datetime: Transformed datetime object.
        """
        if isinstance(raw_value, datetime):
            return raw_value
        time = datetime.strptime(raw_value, "%Y-%m-%d %H:%M:%S %Z")
        return time

    _extract_start_time = validator("start_time", allow_reuse=True, pre=True)(
        transform_time)

    _extract_end_time = validator("end_time", allow_reuse=True, pre=True)(
        transform_time)
