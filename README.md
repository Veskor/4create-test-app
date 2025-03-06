

# 💎 Features

✅ Dockerized PgAdmin to check the db records.\
✅ CRUD APIs (4create Test App).\
✅ Logging Mechanism.\
✅ Testcases TDD with Pytest. \
✅ Seperate Database(Sqlite) and mock session configured for test cases.\
✅ Poetry dependency management and packaging made easy. (Better than pip)


# ⚒️ Techologies Used

- Alembic: For Database Migrations.
- SQLAlchemy: For ORM.
- Pydantic: For Typing or Serialization.
- Pytests: For TDD or Unit Testing.
- Poetry: Python dependency management and packaging made easy. (Better than pip)
- Docker & docker-compose : For Virtualization.
- postgresSQL: Database.
- PgAdmin: To interact with the Postgres database sessions.
- Loguru: Easiest logging ever done.

# 🚀 Up and run in 5 mins 🕙
Make sure you have docker and docker-compose installed [docker installation guide](https://docs.docker.com/compose/install/)
## Step 1
create **.env** file in root folder 4create-test/.env
```
DATABASE_URL=postgresql+psycopg://postgres:password@db:5432/4create_test_db
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=4create_test_db
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
```

## Step 2
```
docker-compose up
```

- Swagger docs on `localhost:8000/docs`
- PgAdmin on `localhost:5050`


# ⚒️ Generate and run Migrations

$ docker-compose run app alembic revision --autogenerate -m "Migration name"

$ docker-compose restart app or $ docker-compose run app alembic upgrade head

# Run tests

$ docker-compose run app pytest
