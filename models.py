# User Schema to validate our expected sender payload
from pydantic import BaseModel
from pydantic.schema import date


class User(BaseModel):
    name: str
    dob: date


class ReceiverUser(BaseModel):
    user: User
    comment: str


class Success(BaseModel):
    success: bool


class BaseError(BaseModel):
    name: str
    status_code: int
    description: str


class ModelValidationError(BaseError):
    name = "Validation Error"
    status_code = 500


class ReceiverSendError(BaseError):
    name = "Receiver Send Error"
    status_code = 404


class ReceiverSendUnexpectedResponse(BaseError):
    name = "Unexpected Response"
