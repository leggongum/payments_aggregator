from pydantic import BaseModel

from typing import Literal
from datetime import datetime

class AggregationRequest(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: Literal['hour', 'day', 'week', 'month']