import sqlite3
from flask import Flask, request, jsonify, send_file, json
from werkzeug import secure_filename
import os
from app.posts import posts

app = Flask(__name__)
app.register_blueprint(posts)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(APP_ROOT, 'static/index.html')

@app.route('/', methods =['GET'])
def index():
    return send_file(INDEX)

# @app.route('/posts', methods =['GET'])
# def posts():
#     return send_file(INDEX)

@app.route('/api/posts', methods =['GET', 'POST'])
def collection():
    if request.method == 'GET':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                SELECT * FROM posts;
                """)
                posts = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        print(posts)
        return json.dumps(posts)
    elif request.method == 'POST':
        data = request.get_json(force=True)
        result = add_post(data['title'], data['body'], data['author'], data['image_url'])
        return jsonify(result)

@app.route('/api/posts/<post_id>', methods = ['GET', 'PATCH', 'DELETE'])
def resource(post_id):
    if request.method == 'GET':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                SELECT * FROM posts WHERE id = ?;
                """, (post_id))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(post)
    elif request.method == 'PATCH':
        data = request.get_json(force=True)
        result = edit_post(data['title'], data['body'], data['author'], data['image_url'], data['id'])
        return jsonify(result)
    elif request.method == 'DELETE':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                DELETE FROM posts WHERE id = ?;
                """, (post_id))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return jsonify(result)

@app.route('/api/posts/<post_id>/votes', methods = ['POST', 'DELETE'])
def votes(post_id):
    if request.method == 'POST':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                UPDATE posts SET vote_count = vote_count + 1 WHERE id = ?;
                """, (post_id))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(result)
    elif request.method == 'DELETE':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                UPDATE posts SET vote_count = vote_count - 1 WHERE id = ?;
                """, (post_id))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(result)

@app.route('/api/posts/<post_id>/comments', methods = ['GET', 'POST'])
def comments(post_id):
    if request.method == 'GET':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * FROM comments WHERE comments.post_id = ?;
                    """, (post_id))
                comments = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(comments)
    elif request.method == 'POST':
        data = request.get_json(force=True)
        result = add_comment(data['content'], data['author'], post_id)
        return jsonify(result)

@app.route('/api/posts/<post_id>/comments/<comment_id>', methods = ['PATCH', 'DELETE'])
def comment(post_id, comment_id):
    if request.method == 'PATCH':
        data = request.get_json(force=True)
        result = edit_comment(data['content'], data['author'], data['id'])
        return jsonify(result)
    elif request.method == 'DELETE':
        try:
            with sqlite3.connect('reddit.db') as connection:
                cursor = connection.cursor()
                cursor.execute("""
                DELETE FROM comments WHERE id = ?;
                """, (comment_id,))
                result = cursor.fetchall()
        except:
            result = {'status': 0, 'message': 'error'}
        return jsonify(result)
        
#HELPER FUNCTIONS

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def add_post(title, body, author, image_url):
    try:
        with sqlite3.connect('reddit.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO posts ( title, body, author, image_url, vote_count) values (?, ?, ?, ?, 0);
            """, ( title, body, author, image_url))
            result = cursor.fetchall()
    except:
        result = {'status': 0, 'message': 'error'}
        return result

def edit_post(title, body, author, image_url, postid):
    try:
        with sqlite3.connect('reddit.db') as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE posts SET title = ?, body = ?, author = ?, image_url = ? WHERE ID = ?;", (title, body, author, image_url, postid))
            result = cursor.fetchall()
    except:
        result = {'status': 0, 'message': 'Error'}
    return result

def add_comment(content, author, postid):
    try:
        with sqlite3.connect('reddit.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO comments (content, author, post_id) values (?, ?, ?);
            """, (content, author, postid))
            result = cursor.fetchall()
    except:
        result = {'status': 0, 'message': 'error'}
        return result

def edit_comment(content, author, commentid):
    try:
        with sqlite3.connect('reddit.db') as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE comments SET content = ?, author = ? WHERE ID = ?;", (content, author, commentid))
            result = cursor.fetchall()
    except:
        result = {'status': 0, 'message': 'Error'}
    return result

if __name__ == '__main__':
    app.debug = True
    app.run()
