import MySQLdb
import os
from dotenv import load_dotenv
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


def getPending():
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM posts where status = 0")
            result = functions.SQLtoJSON([i[0] for i in cursor.description], cursor.fetchall())
        return {"success": True, "data": result}

    except Exception as e:
        return {"success": False, "error": str(e)}
    

def getApproved():
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM posts where status = 1")
            result = functions.SQLtoJSON([i[0] for i in cursor.description], cursor.fetchall())
        return {"success": True, "data": result}

    except Exception as e:
        return {"success": False, "error": str(e)}
    

def getRejected():
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM posts where status = 2")
            result = functions.SQLtoJSON([i[0] for i in cursor.description], cursor.fetchall())
        return {"success": True, "data": result}

    except Exception as e:
        return {"success": False, "error": str(e)}
    

def setStatus(video_id, user_id, status):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE posts SET status = %s WHERE video_id = %s AND user_id = %s",
                (status, video_id, user_id))
        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}
    
