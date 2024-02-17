from dotenv import load_dotenv
import os
import MySQLdb
import json
from utils import functions


load_dotenv()

conn = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "cacert.pem"
  }
)


def store(user_id: int, type: int, video_id: str, views: int, likes: int, comments: int):
    print(f"[history_store] [{video_id}] Storing video details")
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO history (user_id, type, video_id, views, likes, comments) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, type, video_id, views, likes, comments)
            )
            conn.commit()
        print(f"[history_store] [{video_id}] Video details stored successfully")

    except Exception as e:
        print(f"[history_store] [{video_id}] An error occurred: {e}")
        return f"An error occurred: {e}"

    return "Video details stored successfully"

def get(video_id: str, user_id: int, hours = 24):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM history WHERE user_id = %s AND video_id = %s AND date >= DATE_SUB(NOW(), INTERVAL %s HOUR)",
                (user_id, video_id, hours))
            result = functions.SQLtoJSON([i[0] for i in cursor.description], cursor.fetchall())
            result = json.loads(result)
        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        return f"An error occurred: {e}"