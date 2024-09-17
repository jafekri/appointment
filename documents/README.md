# appointment
insert your database information in [../.env] file line_2 like this:
DATABASE_URL='postgres://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/DATABASE_NAME'

install requirements packages that there are in [../requirements.txt] using command below:
```
pip install -r ./requirements.txt
```

make migrations:
```
python manage.py makemigrations
```
```
python manage.py migrate
```

run the project:
```
python manage.py runserver
```

