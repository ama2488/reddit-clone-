const express = require('express');
const router = express.Router();
const knex = require('../db');
const users = require('./users');

router.get('/signup', (req, res, next) => {
  users.createUser(req.body, (error, data) => {
    if (error) {
      res.status(400);
      res.send(error);
    } else {
      res.json(data);
    }
  });
});

router.post('/', (req, res, next) => {
  users.authenticateUser(req.body.username, req.body.password, (error, user) => {
    if (error) {
      res.status(400);
      res.send(error);
    } else {
      res.json(user);
    }
  });
});

module.exports = router;
