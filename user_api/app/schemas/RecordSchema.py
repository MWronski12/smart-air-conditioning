from datetime import datetime
from pydantic import BaseModel


class RecordSchema(BaseModel):
    timestamp: datetime
