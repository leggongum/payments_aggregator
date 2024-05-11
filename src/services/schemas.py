from pydantic import BaseModel
from typing import Literal

class AggregationRequest(BaseModel):
    dt_from: str
    dt_upto: str
    group_type: Literal['hour', 'day', 'week', 'month']