from dotenv import load_dotenv
import os
import MySQLdb
import json

from utils import get_data
from utils import functions
from utils import history

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

def store(user_id: int, type: int, video_id: str, title: str, views: int, likes: int, comments: int):
    print(f"[post_store] [{video_id}] Saving video details")
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO posts (user_id, type, video_id, title, views, likes, comments) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (user_id, type, video_id, title, views, likes, comments)
            )
            conn.commit()
        print(f"[post_store] [{video_id}] Video details stored successfully")

        response = {"success": True}
        return json.dumps(response)

    except Exception as e:
        print(f"[post_store] [{video_id}] An error occurred: {e}")
        response = {"success": False, "error": str(e)}
        return json.dumps(response)

def add(user_id: int, type: int, video_id: str):
    try:
        with conn.cursor() as cursor:
            print("[post_add] Adding post")
            cursor.execute("SELECT * FROM `posts` WHERE `video_id` = %s AND `user_id` = %s", (video_id, user_id))
            post = functions.SQLtoJSON(field_names = [i[0] for i in cursor.description], input = cursor.fetchall())
            post = json.loads(post)
            if len(post) == 0:
                data = fetch(type, video_id)
                if data["success"]:
                    data = data["data"]
                    store(user_id, type, video_id, data["title"], int(data["views"]), int(data["likes"]), int(data["comments"]))
                    fetch(type, video_id)
                    return {"success": True}
            else:
                return {"success": False, "error": "Post already exists"}

    except Exception as e:
        print(f"[post_add] An error occurred: {str(e)}")
        return {"success": False, "error": str(e)}
    
def fetch(type:int ,video_id:str):
    print(f"[post_fetch] [{video_id}] Fetching video details...")
    try:     
        if(type == 1):
            post = get_data.youtube(video_id)
        if(type == 2):
            post = {"success": False, "error": "Tiktok not supported"}
            #post = get_data.tiktok(video_id)

        if type == 3:
            post = {"success": False, "error": "Instagram not supported"}
            #post = get_data.instagram(video_id)

    finally:
        if post["success"]:
            return {"success": True, "data": post["data"]}
        else:
            return {"success": False, "error": post["error"]}
        

    
def get(video_id, user_id):
    try:
        with conn.cursor() as cursor:
            print("[post_get] Getting post")
            cursor.execute("SELECT * FROM `posts` WHERE `video_id` = %s AND `user_id` = %s", (video_id, user_id))
            post = functions.SQLtoJSON(field_names = [i[0] for i in cursor.description], input = cursor.fetchall())
            post = json.loads(post)
            return {"success": True, "data": post}

    except Exception as e:
        print(f"[post_get] An error occurred: {str(e)}")
        return {"success": False, "error": str(e)}
    
    
    
def updateall():
    try:
        with conn.cursor() as cursor:
            print("[post_updateall] Fetching all posts")
            cursor.execute("SELECT `type`, `video_id`, `user_id` FROM `posts`")
            posts = functions.SQLtoJSON(field_names = [i[0] for i in cursor.description], input = cursor.fetchall())
            posts = json.loads(posts)
            print(posts)
            amount = len(posts)
            count = 0	
            for post in posts:
                print(f"[post_updateall] Updating post {count+1} of {amount}")
                data = fetch(post['type'], post['video_id']);
                if data['success']:
                    data = data['data']
                    history.store(post['user_id'], post['type'], post['video_id'], data['views'], data['likes'], data['comments'])
                    count += 1
                    print(f"[post_updateall] Updated {count} of {amount} posts")
                else:
                    print(f"[post_updateall] Failed to fetch data for post {count+1} of {amount}")

        return {"success": True,"posts": amount,"updated": count}

    except Exception as e:
        print(f"[post_updateall] An error occurred: {str(e)}")
        return {"success": False, "error": str(e)}