
exports.seed = function (knex, Promise) {
  const text1 = [
    'One Saturday morning at three,', 'A cheese monger\'s shop in Paree', 'Collapsed to the ground,', ' With a thunderous sound,', 'Leaving only a pile of de brie.',
  ].join('\n\n');

  const text2 = [
    'There was an Old Person of Chester,', 'Whom several small children did pester;', 'They threw some large stones,', 'Which broke most of his bones,', 'And displeased that Old Person of Chester.',
  ].join('\n\n');

  const text3 = [
    'There was an Old Person of Rhodes,', 'Who strongly objected to toads;', 'He paid several cousins,', 'To catch them by the dozens,', 'That futile Old Person of Rhodes.',
  ].join('\n\n');

  const text4 = [
    'There was a young boy from Manassas', 'Who forgot to wash under his glasses', 'And so very soon', 'He looked like a raccoon', 'And scared all the girls in his classes.',
  ].join('\n\n');

  return knex('comments').del()
    .then(() => knex('posts').del())
    .then(() => Promise.all([
      createPost(
          'Cheesy Post',
          text1,
          'Ironic Irma',
          'https://images.pexels.com/photos/211050/pexels-photo-211050.jpeg?h=350&auto=compress',
          new Date(2004, 12, 17)),
      createPost(
          'Oldie but a Goodie',
          text2,
          'Edward Lear',
          'https://img.buzzfeed.com/buzzfeed-static/static/2015-11/19/10/enhanced/webdr13/anigif_enhanced-22345-1447947761-7.gif?downsize=715:*&output-format=auto&output-quality=auto',
          new Date(2011, 11, 11)),
      createPost(
          'Toadally',
          text3,
          'Edward Lear',
          'http://www.birdsandblooms.com/wp-content/uploads/2015/04/RNussbaumerCATO_027406.jpg',
          new Date(2008, 5, 12)),
      createPost(
          'Eye Yi Yi',
          text4,
           'Adeline Foster',
          'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQOqA9Qwb4RzsKO8ZS2XoIsLgh3rzfzhPML1I7ZbgUpqtqNLjLtQ',
          new Date()),
    ]))
    .then(postIds => Promise.all([
      knex('comments').insert({ post_id: postIds[0], content: 'Yikes!', author: 'Mom' }),
      knex('comments').insert({ post_id: postIds[0], content: 'haha', author: 'Bob' }),
      knex('comments').insert({ post_id: postIds[2], content: 'crazy', author: 'Hildegard' }),
    ]));

  function createPost(title, body, author, image_url, created_at) {
    return knex('posts')
      .insert({ title, body, author, image_url, created_at })
      .returning('id')
      .then(ids => ids[0]);
  }
};
