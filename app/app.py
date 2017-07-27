import sqlite3
from flask import Flask, request, jsonify, send_file, json
from werkzeug import secure_filename
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(APP_ROOT, 'static/index.html')
# app.config['INDEX'] = INDEX

@app.route('/', methods =['GET'])
def index():
    return send_file(INDEX)

@app.route('/api/posts/', methods =['GET', 'POST'])
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
            print(posts)
    except:
        result = {'status': 0, 'message': 'error'}
    return json.dumps(posts)

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/posts/<post_id>/comments', methods = ['GET'])
def resource(post_id):
    if request.method == 'GET':
        try:
            with sqlite3.connect('reddit.db') as connection:
                connection.row_factory = dict_factory
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * FROM comments WHERE comments.post_id='post_id';
                    """)
                posts = cursor.fetchall()
                print(posts)
        except:
            result = {'status': 0, 'message': 'error'}
        return json.dumps(posts)


# [(2, 'Oldie but a Goodie', 'There was an Old Person of Chester', 'Edward Lear', 'https://img.buzzfeed.com/buzzfeed-static/static/2015-11/19/10/enhanced/webdr13/anigif_enhanced-22345-1447947761-7.gif?downsize=715:*&output-format=auto&output-quality=auto',
#  0, '11-11-2011', 3, 'crazy', 'Hildegard', '2017-07-27 21:09:20', 2)]


#     pass knex('posts')
#       .then(posts => {
#         return knex('comments')
#           .whereIn('post_id', posts.map(p => p.id))
#           .then((comments) => {
#             const commentsByPostId = comments.reduce((result, comment) => {
#               result[comment.post_id] = result[comment.post_id] || []
#               result[comment.post_id].push(comment)
#               return result
#             }, {})
#             posts.forEach(post => {
#               post.comments = commentsByPostId[post.id] || []
#             })
#             res.json(posts)
#           })
#       })
#       .catch(err => next(err))
# elif request.method == 'POST':
# def add_post(title, body, author, image_url):
#     try:
#         with sqlite3.connect('reddit.db') as connection:
#             cursor = connection.cursor()
#             cursor.execute("""
#                 INSERT INTO posts ( title, body, author, image_url, vote_count) values (?, ?, ?, ?, 0);
#                 """, ( title, body, author, image_url))
#             result = {'status': 1, 'message': 'Post Added'}
#     except:
#         result = {'status': 0, 'message': 'error'}
#     return result
#     pass knex('posts')
#       .insert(params(req))
#       .returning('*')
#       .then(posts => res.json(posts[0]))
#       .catch(err => next(err))
# })
#
# @app.route('/<post_id>', methods = ['GET', 'PATCH', 'DELETE'])
#   def resource(post_id):
#     if request.method == 'GET':
#         pass knex('posts')
#     .where({id: req.params.id})
#     .first()
#     .then(post => res.json(post))
#     .catch(err => next(err))
# elif request.method == 'PATCH':
#     knex('posts')
#       .update(params(req))
#       .where({id: req.params.id})
#       .returning('*')
#       .then(posts => res.json(posts[0]))
#       .catch(err => next(err))
# elif request.method == 'DELETE':
#     knex('posts')
#       .del()
#       .where({id: req.params.id})
#       .then(() => res.end())
#       .catch(err => next(err))
#
# @app.route('/<post_id>/votes', methods = ['POST', 'DELETE'])
#     def resource(post_id):
#     if request.method == 'POST':
#         pass knex('posts')
#           .update('vote_count', knex.raw('vote_count + 1'))
#           .where({id: req.params.id})
#           .then( () => knex('posts').where({id: req.params.id}).first() )
#           .then( post => res.json({vote_count: post.vote_count}))
#           .catch(err => next(err))
#     elif request.method == 'DELETE':
#         pass knex('posts')
#           .update('vote_count', knex.raw('vote_count - 1'))
#           .where({id: req.params.id})
#           .then( () => knex('posts').where({id: req.params.id}).first() )
#           .then( post => res.json({vote_count: post.vote_count}))
#           .catch(err => next(err))

if __name__ == '__main__':
    app.debug = True
    app.run()
