from pydantic import BaseModel, conint


class TaskStatusDTO(BaseModel):
    task_id: int
    status: conint(ge=0, le=100)


class TaskStatusStrDTO(BaseModel):
    task_id: int
    status: str


class AvgTimeDTO(BaseModel):
    seconds: int
    human_readable: str
