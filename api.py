from flask import Flask, request, jsonify
from utils import post, history, statistics, status

app = Flask(__name__)

@app.route('/api/post/updateall', methods=['GET']) # Update all posts  and saves it to history
def updateall():
    job = post.updateall()
    if job['success']:
        return {'success': True, 'posts': job['posts'], 'updated': job['updated']}
    else:
        return {'success': False, 'error': job['error']}



@app.route('/api/post', methods=['PATCH']) # Fetch a post (gets fresh data)
def postfetch():
    if request.is_json:
        data = request.get_json()

        type = data.get('type')
        video_id = data.get('video_id')

        job = post.fetch(type, video_id)
        if job['success']:
            return {'success': True, 'data': job['data']}
        else:
            return {'success': False, 'error': job['error']}
    else:
        print(request)
        return {'success': False, 'error': 'Invalid JSON, require video_id and type'}, 400



@app.route('/api/post', methods=['GET']) # Get a post from database
def PostGet():
    if request.is_json:
        data = request.get_json()

        user_id = data.get('user_id')
        video_id = data.get('video_id')

        job = post.get(video_id, user_id)
        if job['success']:
            return {'success': True, 'data': job['data']}, 200
        else:
            return {'success': False, 'error': job['error']}, 400
    else:
        return {'success': False, 'error': 'Invalid JSON, require video_id and type'}, 400
    

    
@app.route('/api/post', methods=['POST']) # Add a post to database
def PostAdd():
    if request.is_json:
        data = request.get_json()
        user_id = data.get('user_id')
        type = data.get('type')
        video_id = data.get('video_id')

        job = post.add(user_id, type, video_id)
        if job['success']:
            return {'success': True}, 200
        else:
            return {'success': False, "error" : job["error"]}, 400
    else:
        return {'success': False, 'error': 'Invalid JSON, require video_id, user_id'}, 400



@app.route('/api/history', methods=['GET']) # Get history of a post
def GetHistory():
    if request.is_json:
        data = request.get_json()
        video_id = data.get('video_id')
        user_id = data.get('user_id')
        hours = data.get('hours')
        job = history.get(video_id, user_id, hours)
        if job['success']:
            return {'success': True, 'data': job['data']}
        else:
            return {'success': False, 'error': job['error']}
    else:
            return {'success': False, 'error': 'Invalid JSON, require video_id, user_id, hours, history (true or false)'}, 400
    

    


# get all history of posts
@app.route('/api/user/statistics', methods=['GET'])
def GetUserStatistic():
    if request.is_json:
        data = request.get_json()
        user_id = data.get('user_id')
        hours = data.get('hours')
        history = data.get('history')

        job = statistics.get(user_id, hours, history)["data"]
        return {'success': True, 'data': job}
    else:
        return {'success': False, 'error': 'Invalid JSON, require user_id INT, hours INT, history BOOL'}, 400
    




@app.route('/api/post/status', methods=['PATCH']) # Set status of a post
def SetStatus():
    if request.is_json:
        data = request.get_json()
        video_id = data.get('video_id')
        status1 = data.get('status')
        user_id = data.get('user_id')
        job = status.setStatus(video_id, user_id, status1)
        if job['success']:
            return {'success': True}
        else:
            return {'success': False, 'error': job['error']}
    else:
        return {'success': False, 'error': 'Invalid JSON, require video_id, status'}, 400
    
@app.route('/api/post/status/pending', methods=['GET']) # Get all pending posts
def GetPending():
    job = status.getPending()
    if job['success']:
        return {'success': True, 'data': job['data']}
    else:
        return {'success': False, 'error': job['error']}

@app.route('/api/post/status/approved', methods=['GET']) # Get all approved posts
def GetApproved():
    job = status.getApproved()
    if job['success']:
        return {'success': True, 'data': job['data']}
    else:
        return {'success': False, 'error': job['error']}

@app.route('/api/post/status/rejected', methods=['GET']) # Get all rejected posts
def GetRejected():
    job = status.getRejected()
    if job['success']:
        return {'success': True, 'data': job['data']}
    else:
        return {'success': False, 'error': job['error']}
    

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')

