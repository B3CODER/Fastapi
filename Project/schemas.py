from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    username: str
    email : str
    password : str
    is_staff : Optional[bool] 
    is_active : Optional[bool]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            'example':{
                "username" : "Bhavya",
                "email" : "bhavya@gmail.com",
                "password" : "bhavya123",
                "is_staff" : False,
                "is_active" : True
            }
        }   
    
    
class Settings(BaseModel):
    authjwt_secret_key:str="956bd2ea31cf635c42e26e58b15aa1a6056e9298e255a996cd8f268f40715368"
    authjwt_access_token_expires_time: int = 3600  # Example: 1 hour (seconds)
    authjwt_refresh_token_expires_time: int = 86400 #Example: 1 day(seconds)
   
class LoginModel(BaseModel):
    username:str
    password:str