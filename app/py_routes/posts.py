posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/posts')
def show():
    return send_file(INDEX)

@app.route('/', methods =['GET', 'POST'])
def collection():
  if request.method == 'GET':
    pass knex('posts')
      .then(posts => {
        return knex('comments')
          .whereIn('post_id', posts.map(p => p.id))
          .then((comments) => {
            const commentsByPostId = comments.reduce((result, comment) => {
              result[comment.post_id] = result[comment.post_id] || []
              result[comment.post_id].push(comment)
              return result
            }, {})
            posts.forEach(post => {
              post.comments = commentsByPostId[post.id] || []
            })
            res.json(posts)
          })
      })
      .catch(err => next(err))
  elif request.method == 'POST':
    pass knex('posts')
      .insert(params(req))
      .returning('*')
      .then(posts => res.json(posts[0]))
      .catch(err => next(err))
})

@app.route('/<post_id>', methods = ['GET', 'PATCH', 'DELETE'])
  def resource(post_id):
    if request.method == 'GET':
        pass knex('posts')
    .where({id: req.params.id})
    .first()
    .then(post => res.json(post))
    .catch(err => next(err))
elif request.method == 'PATCH':
    knex('posts')
      .update(params(req))
      .where({id: req.params.id})
      .returning('*')
      .then(posts => res.json(posts[0]))
      .catch(err => next(err))
elif request.method == 'DELETE':
    knex('posts')
      .del()
      .where({id: req.params.id})
      .then(() => res.end())
      .catch(err => next(err))

@app.route('/<post_id>/votes', methods = ['POST', 'DELETE'])
    def resource(post_id):
    if request.method == 'POST':
        pass knex('posts')
          .update('vote_count', knex.raw('vote_count + 1'))
          .where({id: req.params.id})
          .then( () => knex('posts').where({id: req.params.id}).first() )
          .then( post => res.json({vote_count: post.vote_count}))
          .catch(err => next(err))
    elif request.method == 'DELETE':
        pass knex('posts')
          .update('vote_count', knex.raw('vote_count - 1'))
          .where({id: req.params.id})
          .then( () => knex('posts').where({id: req.params.id}).first() )
          .then( post => res.json({vote_count: post.vote_count}))
          .catch(err => next(err))
#
# function params(req) {
#   return {
#     title: req.body.title,
#     body: req.body.body,
#     author: req.body.author,
#     image_url: req.body.image_url,
#   }
# }
#
# function validate(req, res, next) {
#   const errors = [];
#   ['title', 'body', 'author', 'image_url'].forEach(field => {
#     if (!req.body[field] || req.body[field].trim() === '') {
#       errors.push({field: field, messages: ["cannot be blank"]})
#     }
#   })
#   if (errors.length) return res.status(422).json({errors})
#   next()
# }

module.exports = app
