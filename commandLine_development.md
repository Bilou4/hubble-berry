# Some command lines for development

## Setting up a development environment

### Installing

You have the possibility to develop on another computer than your raspberry pi, you just won't be able to test functionnalities for the camera.

+ After cloning the project, go into the directory `cd hubble-berry`.
+ If virtualenv is not installed on your Raspberry PI `pip3 install virtualenv`
+ create a virtual environment (your python version must be greater than 3.6) `virtualenv --python=/usr/local/bin/python3.7 hubble-berry-project`
+ Activate the environment `. activate`
+ Execute the installation file `./installation.sh`
+ To finish, you can start the application

```sh
FLASK_APP=main.py FLASK_ENV=development flask run --port 8000 --with-threads # just on localhost
FLASK_APP=main.py FLASK_ENV=development flask run --port 8000 --host=0.0.0.0 --with-threads # to all active interfaces
```

if everything worked properly, you should be able to reach the first page.

![First_page](./img/first_page.png)

+ To leave the virtual environment `deactivate`
+ If you are using vscode and there is a problem with the virtual environment https://stackoverflow.com/questions/54106071/how-to-setup-virtual-environment-for-python-in-vs-code


## To manage the database 

### After modifying models

```sh
FLASK_APP=main.py flask db migrate -m "<explicative message>"
FLASK_APP=main.py flask db upgrade
```

### To have at least one admin

Open the SQLite table : `appFolder/app.db`

```SQL
INSERT INTO `role` (id, name) VALUES ([id_of_the_user_who_will_be_admin],"admin");
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

### In the end, compile to make the runtime easier

```sh
pybabel compile -d appFolder/translations
```
