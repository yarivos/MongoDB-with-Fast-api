from typing import Optional, List, Union, Literal
from pydantic import BaseModel, validator


class Drone(BaseModel):
    """
    Represents a drone object with attributes including its ID, name, status,
    current mission ID, and possible missions IDs.
    """

    id: int

    name: str

    status: Literal['available', 'on-mission', 'pending']

    current_mission_id: Optional[int] = None

    possible_missions_ids: List[int] = []

    @classmethod
    def transform_possible_missions_ids(cls, raw_value: str):
        """
        Class method to transform raw possible missions IDs into a list of integers.

        Parameters:
            raw_value (str): Raw string containing mission IDs.

        Returns:
            List[int]: List of integers representing mission IDs.
        """
        if isinstance(raw_value, list):
            return raw_value
        elif isinstance(raw_value, str):
            value_as_list = raw_value.replace("[", "").replace("]", "").split(",")
            missions_ids = []
            for value in value_as_list:
                missions_ids.append(int(value) if value is not None else None)
            return missions_ids
        else:
            return [int(raw_value)]

    _extract_possible_missions_ids = validator("possible_missions_ids", allow_reuse=True, pre=True)(
        transform_possible_missions_ids)

    @classmethod
    def transform_current_mission_id(cls, raw_value: Union[int, str]):
        """
        Class method to transform raw current mission ID into an integer.

        Parameters:
            raw_value (Union[int, str]): Raw value of the current mission ID.

        Returns:
            int: Transformed current mission ID.
        """
        try:
            result = int(raw_value)
        except:
            result = None
        return result

    _extract_current_mission_id = validator("current_mission_id", allow_reuse=True, pre=True)(
        transform_current_mission_id)
