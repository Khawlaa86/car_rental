# This will contain the configuration settings
# config/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    DATABASE_PATH = "database/car_rental.db"
