import base64, hashlib, hmac, json, os, time
from app.core.config import settings

def hash_password(password: str) -> str:
    salt=os.urandom(16); digest=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
    return "scrypt$%s$%s" % (base64.urlsafe_b64encode(salt).decode(),base64.urlsafe_b64encode(digest).decode())
def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme,salt,digest=encoded.split("$"); actual=hashlib.scrypt(password.encode(),salt=base64.urlsafe_b64decode(salt),n=2**14,r=8,p=1)
        return scheme=="scrypt" and hmac.compare_digest(base64.urlsafe_b64encode(actual).decode(),digest)
    except Exception: return False

def create_access_token(subject: str, role: str="learner") -> str:
    now=int(time.time()); header={"alg":"HS256","typ":"JWT"}; payload={"sub":subject,"role":role,"iat":now,"exp":now+settings.access_token_minutes*60}
    enc=lambda obj: base64.urlsafe_b64encode(json.dumps(obj,separators=(",",":")).encode()).rstrip(b"=").decode()
    signing=f"{enc(header)}.{enc(payload)}"; sig=base64.urlsafe_b64encode(hmac.new(settings.secret_key.encode(),signing.encode(),hashlib.sha256).digest()).rstrip(b"=").decode()
    return f"{signing}.{sig}"
def decode_access_token(token: str) -> dict:
    try:
        a,b,c=token.split("."); signing=f"{a}.{b}"; expected=base64.urlsafe_b64encode(hmac.new(settings.secret_key.encode(),signing.encode(),hashlib.sha256).digest()).rstrip(b"=").decode()
        if not hmac.compare_digest(c,expected): raise ValueError("Invalid signature")
        payload=json.loads(base64.urlsafe_b64decode(b+"="*(-len(b)%4)))
        if payload["exp"] < time.time(): raise ValueError("Expired token")
        return payload
    except Exception as exc: raise ValueError("Invalid or expired token") from exc
