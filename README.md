# project-galaxy-backend
This will be the backend for project galaxy. <br />
Written using python/flask/postgresql <br />

## Setting up PostgreSQL on test environment
```
1. brew install postgresql
2. pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
3. sudo psql postgres
4. create database project-galaxy-test
    CREATE DATABASE
    \q
5. export DATABASE_URL="postgresql://localhost/project-galaxy-test"
```

## Setting up Bash Variables for Test S3 Bucket
```
nano ~/.bash_profile

Add these following exports:

export PROJECT_GALAXY_TEST_BUCKET=project-galaxy-test
export AWS_SECRET_KEY=BLAHBLAHBLAH
export AWS_ACCESS_KEY=FILLIN
```