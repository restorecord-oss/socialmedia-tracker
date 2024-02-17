from utils import history, user
import json


def get(user_id: int, hours = 24):
    data = user.getPosts(user_id)["data"]
    data = json.loads(data)
    hours_views = 0; hours_comments = 0; hours_likes = 0; hours_points = 0; post_history = []


    for post in data:
        post_history.append({
            "video_id": post["video_id"],
            "title": post["title"],
            "views": post["views"],
            "comments": post["comments"],
            "likes": post["likes"],
            "status": post["status"],
            "history": history.get(post["video_id"], user_id, hours)["data"]
        })
    
    for post in post_history:
        views = []
        comments = []
        likes = []
        for post1 in post["history"]: 
            views.append(post1["views"])
            comments.append(post1["comments"])
            likes.append(post1["likes"])
        views_min = min(views) if views else 0
        views_max = max(views) if views else 0
        comments_min = min(comments) if comments else 0
        comments_max = max(comments) if comments else 0
        likes_min = min(likes) if likes else 0
        likes_max = max(likes) if likes else 0
        hours_views += views_max - views_min
        hours_comments += comments_max - comments_min
        hours_likes += likes_max - likes_min

    return {
        "data": {"history": post_history, "last_hours".format(hours): { "views": hours_views, "comments": hours_comments, "likes": hours_likes, "points": hours_points}},"success": True}
