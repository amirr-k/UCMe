import os
import secrets
import redis
import emails
from datetime import datetime, timedelta
from typing import Optional

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

def generateVerificationCode():
    return str(secrets.randbelow(1000000)).zfill(6)

def storeVerificationCode(email: str, code: str, expiresIn: int = 300):
    try:
        key = f"verification:{email}"
        redis_client.setex(key, expiresIn, code)
        return True
    except Exception:
        return False

def getVerificationCode(email: str) -> Optional[str]:
    try:
        key = f"verification:{email}"
        return redis_client.get(key)
    except Exception:
        return None

def deleteVerificationCode(email: str) -> bool:
    try:
        key = f"verification:{email}"
        redis_client.delete(key)
        return True
    except Exception:
        return False

def sendVerificationEmail(email: str, code: str):
    try:
        smtpOptions = {
            "host": os.getenv('SMTP_HOST', 'smtp.gmail.com'),
            "port": int(os.getenv('SMTP_PORT', 587)),
            "user": os.getenv('SMTP_USER'),
            "password": os.getenv('SMTP_PASSWORD'),
            "tls": True,
        }
        
        htmlContent = f"""
        <html>
        <body>
            <h2>Welcome to UCMe!</h2>
            <p>Your verification code is: <strong>{code}</strong></p>
            <p>This code will expire in 5 minutes.</p>
            <p>Please do not share this code with anyone.</p>
        </body>
        </html>
        """         
        
        message = emails.Message(
            subject="Your UCMe Verification Code",
            html=htmlContent,
            mail_from=(os.getenv('APP_NAME', 'UCMe'), os.getenv('SMTP_USER'))
        )
        
        response = message.send(
            to=email,
            smtp=smtpOptions
        )
        
        return response.status_code == 250
    except Exception as e:
        print(f"Email sending error: {e}")
        return False 