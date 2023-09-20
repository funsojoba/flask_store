import datetime
import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

# DATABASE
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://postgres:{postgres_password}@db:5432/{postgres_db}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = 0
PROPAGATE_EXCEPTIONS = 1

# JWT
JWT_TOKEN_TTL_HOURS = 3
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=JWT_TOKEN_TTL_HOURS)
