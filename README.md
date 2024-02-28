# Flask-API

## Description

Flask API Development for Test Case Management.

## Output

Unit tests
![Alt text](img/unitTest.PNG)

Sqlite
![Alt text](img/DsqliteB.PNG)

## Run

you can fill the data in sqlite , can retrive the data , update and delete the data

run the code (run.py)

select the unit test you want (get , delete , post , put) from (tests/test_api.py)

```bash
pytest tests/test_api.py
```

go to another git bash to show the data (sqlite)

```bash
sqlite3 test_cases.db
```

then write SELECT \* FROM test_cases;

you will see the all the data (id , name , description , execution result)
