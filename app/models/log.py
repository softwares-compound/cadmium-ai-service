from pydantic import BaseModel

class Log(BaseModel):
    id: str
    org_id: str
    app_id: str
    message: str
    level: str
    timestamp: str
