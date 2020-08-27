module.exports = {
  "type": "postgres",
  "host": "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "password",
  "database": "StepByStep",
  "entities": [
    __dirname + "/src/entities/*.ts"
  ],
  "synchronize": true
}
