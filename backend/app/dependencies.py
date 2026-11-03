from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.core.security import decode_access_token
bearer=HTTPBearer(auto_error=False)
def current_user(credentials: HTTPAuthorizationCredentials|None=Depends(bearer), db:Session=Depends(get_db)):
    if not credentials: raise HTTPException(401,"Authentication required")
    try: uid=int(decode_access_token(credentials.credentials)["sub"])
    except Exception: raise HTTPException(401,"Invalid or expired token")
    user=db.get(User,uid)
    if not user or not user.is_active: raise HTTPException(401,"User unavailable")
    return user
def admin_user(user:User=Depends(current_user)):
    if user.role!="admin": raise HTTPException(403,"Administrator access required")
    return user
