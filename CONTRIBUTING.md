# Installation

1. Clone repository.
2. Start `git-flow`
2. Make virtual env and install requirements.
3. Create docker databases.
4. Create tables with data & superuser.

```bash
$ git clone https://github.com/lecovi/dumpmyjson.git
$ cd flaskngo
$ git checkout master   # Creating local master branch
$ git checkout develop  # Going back to develop branch
$ git flow init -d
$ mkvirtualenv -p $(which python3) dumpmyjson
$ pip install -r requirements/development.txt
$ docker run --name dumpmyjson-db -e POSTGRES_PASSWORD=lecovi.dumpmyjson -e POSTGRES_USER=lecovi -e POSTGRES_DB=dumpmyjson -p 5432:5432 -d postgres
$ cp .env.dist .env     # Make sure to change your variables!
$ ./manage.py db create -s
```

# Documentation

1. Create html documentation

```bash
$ ./manage.py make_docs -v -s
```
 * `-v`: verbose make command from Sphinx
 * `-s`: opens index.html from documentation

# Running application

1. Run Flask application

```bash
$ ./manage.py runserver --host 0.0.0.0 --port 8000
```

# Development

We use [git-flow](http://nvie.com/posts/a-successful-git-branching-model/) 
as our development model. You always must create a new feature from 
`develop` branch. You are responsible to merge your feature into 
`develop`. 
 
1. Make sure your Docker DB is running vía command line or *Portainer*.
2. Create new feature with `git-flow`.
 
```bash
$ docker start dumpmyjson-db
$ git flow feature start awesome_new_feature
```

or use `new_package` option in `manage.py`. This will ask you for package
name, create package directory with some python files to use as a template
and create a new feature branch using `git-flow`.

```bash
$ docker start flaskngo-db
$ ./manage.py new_package
```
 * `-n`: package name
 * `-d`: package description

# Deploy

1. Clone repo
2. Create virtualenv with production requirements.
3. Create Docker DB.
4. Initialize Tables.
5. Configure Supervisor

```bash
$ git clone https://github.com/lecovi/dumpmyjson.git
$ cd dumpmyjson
$ mkvirtualenv -p $(which python3) dumpmyjson
(dumpmyjson) $ pip install -r requirements/production.txt
$ docker run --name dumpmyjson-db -e POSTGRES_PASSWORD=lecovi.dumpmyjson -e POSTGRES_USER=lecovi -e POSTGRES_DB=dumpmyjson -p 5432:5432 -d postgres
$ cp .env.dist .env     # Make sure to change your variables!
$ ./manage.py db create
$ cp ./utils/deploy/supervisor/dumpmyjson.conf /etc/supervisor/conf.d/dumpmyjson.conf
```

## Test

1. Run application with gunicorn

```bash
(dumpmyjson) $ gunicorn --bind 0.0.0.0:8000 --workers 2 wsgi:app
```