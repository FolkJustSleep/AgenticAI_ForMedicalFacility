from pydantic import BaseModel

class ChatTestResponse(BaseModel):
    response: str
    
class ChatTestRequest(BaseModel):
    message: str