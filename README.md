# Users Microservice

## What do you need

### Docker-ce

**Version:** Docker version 17.09.1-ce, build 19e2cf6
Downlad from [here](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)

### Docker-compose

**Version:** docker-compose version 1.18.0-rc2, build 189468b
Download from [here](https://docs.docker.com/compose/install/)

### Docker-machine

**Version:** docker-machine version 0.13.0, build 9ba6da9
Download from [here](docker-machine version 0.13.0, build 9ba6da9)


## Workflow

### VirtualEnv

```bash
$ python3.6 -m venv env
$ source env/bin/activate
```

### Docker common commands

Build the images:
```bash
$ docker-compose build
```

Run the containers:
```bash
$ docker-compose up -d
```

Create the database:
```bash
$ docker-compose run users-service python manage.py recreate_db
```

Seed the database:
```bash
$ docker-compose run users-service python manage.py seed_db
```

Run the tests:
```bash
$ docker-compose run users-service python manage.py test
```

#### Deploy to production with AWS

Create aws host:
```bash
docker-machine create --driver amazonec2 --amazonec2-access-key <key> --amazonec2-secret-key <secresecrett> aws
```

Active host and point the docker client at it:
```bash
$ docker-machine env aws
$ eval $(docker-machine env aws)
```

List running machines setting timeout to 60 seconds:
```bash
$ docker-machine ls -t 60
```

Spin up the containers, create the database, seed, and run the tests:
```bash
$ docker-compose -f docker-compose-prod.yml up -d --build
$ docker-compose -f docker-compose-prod.yml run users-service python manage.py recreate_db
$ docker-compose -f docker-compose-prod.yml run users-service python manage.py seed_db
$ docker-compose -f docker-compose-prod.yml run users-service python manage.py test
```

### Postgres

Access the database via psql:
```bash
$ docker exec -ti users-db psql -U postgres -W
```

Then, you can connect to db and run SQL queries:
```bash
# \c users_dev
# select * from users;
```

### Environment variables

```bash
$ source env/bin/activate
(env)$ export REACT_APP_USERS_SERVICE_URL=http://localhost 
(env)$ export APP_SETTINGS=project.config.DevelopmentConfig
(env)$ export DATABASE_URL=postgres://postgres:postgres@localhost:5432/users_dev
(env)$ export DATABASE_TEST_URL=postgres://postgres:postgres@localhost:5432/users_test
(env)$ python manage.py test
```

### Flask Migrator

Change the model and migrate:

```bash
(env)$ python manage.py db init
(env)$ python manage.py db migrate
(env)$ python manage.py db upgrade
```
