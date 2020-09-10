# Some command lines for development

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

### At the end, compile to make the runtime easier

```sh
pybabel compile -d appFolder/translations
```
