import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return
    try:
        user = 'root'
        password = 'Ranjithkumar@123'
        host = 'localhost'
        port = 3306
        db_name = 'nightvision_guardian_db'

        connection = pymysql.connect(host=host, port=port, user=user, password=password)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Database '{db_name}' created or already exists.")
    except Exception as e:
        print(f"Failed to create database: {e}")

if __name__ == "__main__":
    create_database()
