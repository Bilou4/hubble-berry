# hubble-berry


## To activate the env

```sh
. activate
```
## To start the app with Flask

```sh
FLASK_APP=main.py FLASK_ENV=development flask run --port 8000 --with-threads <br>
FLASK_APP=main.py FLASK_ENV=development flask run --port 8000 --host=0.0.0.0 --with-threads
```

## To manage the database after changing models

```sh
FLASK_APP=main.py flask db migrate -m "<message explicatif>"
FLASK_APP=main.py flask db upgrade
```


## To see requirements for the env

```sh
pip3 freeze > requirements.txt
```

## To leave the env

```sh
deactivate
```

## If problem with vscode venv

> https://stackoverflow.com/questions/54106071/how-to-setup-virtual-environment-for-python-in-vs-code

<br>

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
