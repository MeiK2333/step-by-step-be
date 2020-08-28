module.exports = {
  "type": "postgres",
  "host": process.env.POSTGRES_HOST || "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "password",
  "database": "StepByStep",
  "entities": [
    __dirname + "/src/entities/*.ts"
  ],
  "synchronize": true
}
