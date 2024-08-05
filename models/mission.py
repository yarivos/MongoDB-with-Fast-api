from pydantic import BaseModel, Field


class Mission(BaseModel):
    """
    Represents a mission object with attributes including its ID, trajectory ID,
    duration, and priority level.
    """

    id: int

    trajectory_id: int

    duration: int = Field(ge=0)

    priority: int = Field(ge=0, le=10)
