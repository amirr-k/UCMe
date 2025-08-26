import os
import secrets
import redis
import emails
import logging
from datetime import datetime, timedelta
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = None
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=0,
        decode_responses=True,
        socket_connect_timeout=5,  # 5 second timeout
        socket_timeout=5
    )
    # Test connection
    redis_client.ping()
    logger.info("Redis connection established successfully")
except Exception as e:
    logger.warning(f"Redis connection failed: {e}. Verification codes will not be stored persistently.")
    redis_client = None

def generateVerificationCode():
    return str(secrets.randbelow(1000000)).zfill(6)

def storeVerificationCode(email: str, code: str, expiresIn: int = 300):
    if redis_client is None:
        logger.warning(f"Redis not available. Verification code for {email}: {code} (expires in {expiresIn}s)")
        return True 
    
    try:
        key = f"verification:{email}"
        redis_client.setex(key, expiresIn, code)
        return True
    except Exception as e:
        logger.error(f"Failed to store verification code in Redis: {e}")
        return False

def getVerificationCode(email: str) -> Optional[str]:
    if redis_client is None:
        logger.warning(f"Redis not available. Cannot retrieve verification code for {email}")
        return None
    
    try:
        key = f"verification:{email}"
        return redis_client.get(key)
    except Exception as e:
        logger.error(f"Failed to get verification code from Redis: {e}")
        return None

def deleteVerificationCode(email: str) -> bool:
    if redis_client is None:
        logger.warning(f"Redis not available. Cannot delete verification code for {email}")
        return True
    
    try:
        key = f"verification:{email}"
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Failed to delete verification code from Redis: {e}")
        return False

def sendVerificationEmail(email: str, code: str):
    # Check if SMTP is properly configured
    smtp_host = os.getenv('SMTP_HOST')
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    # If SMTP is not configured, log the code instead
    if not all([smtp_host, smtp_user, smtp_password]):
        logger.info(f"SMTP not configured. Verification code for {email}: {code}")
        logger.info("To enable email sending, set SMTP_HOST, SMTP_USER, and SMTP_PASSWORD environment variables")
        logger.info("For SMTP2Go: SMTP_HOST=mail.smtp2go.com, SMTP_PORT=2525")
        return True  # Return True to avoid breaking the flow
    
    try:
        # Get SMTP configuration with defaults
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_tls = os.getenv('SMTP_TLS', 'true').lower() == 'true'
        smtp_ssl = os.getenv('SMTP_SSL', 'false').lower() == 'true'
        
        smtpOptions = {
            "host": smtp_host,
            "port": smtp_port,
            "user": smtp_user,
            "password": smtp_password,
        }
        
        # Configure TLS/SSL based on port and settings
        if smtp_ssl:
            smtpOptions["ssl"] = True
        elif smtp_tls:
            smtpOptions["tls"] = True
        
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
            mail_from=("UCMe", "no-reply@amirkiadi.com")
        )
        
        response = message.send(
            to=email,
            smtp=smtpOptions
        )
        
        if response.status_code == 250:
            logger.info(f"Verification email sent successfully to {email}")
            return True
        else:
            logger.error(f"Failed to send email to {email}. Status: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Email sending error for {email}: {e}")
        # Fallback: log the code instead of failing
        logger.info(f"Fallback: Verification code for {email}: {code}")
        return True  # Return True to avoid breaking the flow 