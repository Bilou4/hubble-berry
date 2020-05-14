# hubble-berry


## To activate the env

```sh
. activate
```
## To start the app with Flask

```sh
FLASK_APP=app.py FLASK_ENV=development flask run --port 8080
```
If it is all configured in Code

```sh
python3 app.py
```

## To see requirements for the env

```sh
pip3 freeze > requirements.txt
```

## To leave the env

```sh
deactivate
```