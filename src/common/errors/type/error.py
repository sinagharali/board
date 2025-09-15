from pydantic import BaseModel


class ErrorObject(BaseModel):
    code: str
    message: str
    status_code: int

    class Config:
        frozen = True
