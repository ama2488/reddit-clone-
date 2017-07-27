
exports.up = function (knex, Promise) {
  return knex.schema.createTable('users', (table) => {
    table.increments();
    table.string('username').notNullable();
    table.password('password').notNullable();
    table.dateTime('created_at').notNullable().defaultTo(knex.fn.now());
  });
};

exports.down = function (knex, Promise) {
  return knex.schema.dropTable('users');
};
