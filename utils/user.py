import MySQLdb
import os
from dotenv import load_dotenv
import json
from utils import functions




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


def getPosts(user_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM posts WHERE user_id = %s",
                (user_id,))
            result = functions.SQLtoJSON([i[0] for i in cursor.description], cursor.fetchall())
        return {"success": True, "data": result}

    except Exception as e:
        return {"success": False, "error": str(e)}