from passlib.context import CryptContext
import random
import time
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
CODE_LENGTH = 50
CHARS = "123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHARS_LENGTH = len(CHARS)

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_random_code():
    code = ""
    random.seed(time.time())
    random.seed(random.randint(0,10000000))
    for _ in range(CODE_LENGTH):
        code += CHARS[random.randint(0, CHARS_LENGTH-1)]
    return code
