# hubble-berry


## To activate the env

```sh
. activate
```
## To start the app with Flask

```sh
FLASK_APP=main.py FLASK_ENV=development flask run --port 8000
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
