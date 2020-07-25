# hubble-berry


## To activate the env

```sh
. activate
```
or leave the env

```sh
deactivate
```

If there is a problem with vscode venv

> https://stackoverflow.com/questions/54106071/how-to-setup-virtual-environment-for-python-in-vs-code

<hr>

## Install dependencies
```sh
./installation.sh
```
To see requirements for the env

```sh
pip3 freeze > requirements.txt
```
<hr>

## To start the app with Flask

```sh
FLASK_APP=main.py FLASK_ENV=development flask run --port 8000 --with-threads # just on localhost
FLASK_APP=main.py FLASK_ENV=development flask run --port 8000 --host=0.0.0.0 --with-threads # to all active interfaces
```
<hr>

## To manage the database after changing models

```sh
FLASK_APP=main.py flask db migrate -m "<explicative message>"
FLASK_APP=main.py flask db upgrade
```

## Add user in sqlite

```sql
-- SQLite
INSERT INTO `user` (id, username, email, password_hash, role_id)
VALUES (1, 'test','bonjour@mail.fr', 'pbkdf2:sha256:150000$E7IKksJJ$7efee81204352ecfe031ae666716a9475cfd0a550658097e8181f388e6050e54', 1);
INSERT INTO `role` (id, name)
VALUES (1,"admin");
INSERT INTO `role` (id, name)
VALUES (2,"user");
```

<hr>

## Manage languages

### Extract information from all files

```sh
pybabel extract -F babel.cfg -k _l -o messages.pot . 
```

### Update files for existing languages

```sh
pybabel update -i messages.pot -d appFolder/translations
```

### If you need to create files for another language

```sh
pybabel init -i messages.pot -d appFolder/translations -l fr
```

### At the end, compile to make the runtime easier

```sh
pybabel compile -d appFolder/translations
```

<hr>

## Use of external projects or tutorial

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

https://blog.miguelgrinberg.com/post/video-streaming-with-flask

https://galleriajs.github.io/

http://www.astrosurf.com/luxorion/Images/messier-catalog-mike-keith.jpg

https://www.ligo.caltech.edu/video/ligo20160211v2

https://medium.com/@galea/python-logging-example-with-color-formatting-file-handlers-6ee21d363184

