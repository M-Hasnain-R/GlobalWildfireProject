
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WildfireRecord(BaseModel):

    # Reject unexpected columns
    model_config = ConfigDict(
    extra="forbid",
    allow_inf_nan=False
)

    # Geographic coordinates
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    # Brightness and pixel measurements
    bright_ti4: float = Field(gt=0)
    scan: float = Field(gt=0)
    track: float = Field(gt=0)

    # Date and time
    acq_date: date
    acq_time: str

    # Satellite information
    satellite: str
    instrument: str

    # Detection information
    confidence: Literal["l", "n", "h"]
    version: str

    # Fire measurements
    bright_ti5: float = Field(gt=0)
    frp: float = Field(gt=0)

    # Day or night
    daynight: Literal["D", "N"]
