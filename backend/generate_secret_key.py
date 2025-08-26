import secrets
import string

def generate_secret_key(length=64):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("Generated Secret Keys:")
    print("=" * 50)
    for i in range(3):
        key = generate_secret_key()
        print(f"Option {i+1}: {key}")
    print("=" * 50)
    print("Copy one of these keys to your .env file as SECRET_KEY") 
import string

def generate_secret_key(length=64):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("Generated Secret Keys:")
    print("=" * 50)
    for i in range(3):
        key = generate_secret_key()
        print(f"Option {i+1}: {key}")
    print("=" * 50)
    print("Copy one of these keys to your .env file as SECRET_KEY") 