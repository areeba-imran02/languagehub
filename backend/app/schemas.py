from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Literal
class RegisterIn(BaseModel): email: EmailStr; password: str=Field(min_length=10,max_length=128); display_name: str=Field(default="Learner",max_length=100)
class LoginIn(BaseModel): email: EmailStr; password: str=Field(min_length=1,max_length=128)
class TokenOut(BaseModel): access_token: str; token_type: str="bearer"
class UserOut(BaseModel): model_config=ConfigDict(from_attributes=True); id:int; email:str; role:str
class WordIn(BaseModel): word:str=Field(min_length=1,max_length=200); translation:str=""; definition:str=""; example:str=""; language_code:str="en"
class WordOut(BaseModel): model_config=ConfigDict(from_attributes=True); id:int; word:str; translation:str; definition:str; example:str; language_code:str; mastery:int
class TutorIn(BaseModel): message:str=Field(min_length=1,max_length=5000); target_language:str="ur"; known_language:str="en"; explanation_language:str="en"; mode:Literal["fast","smart","fallback"]="fast"
class TutorOut(BaseModel): reply:str; provider:str; configured:bool
class ProgressIn(BaseModel):
    activity_type: str = Field(min_length=1, max_length=40)
    activity_id: str = Field(default="", max_length=100)
    completed: bool = False
    score: int | None = Field(default=None, ge=0, le=100)
    minutes_spent: int = Field(default=0, ge=0, le=1440)
