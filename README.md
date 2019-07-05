# adjask
adjask provides single endpoint `/metrics` to render desired dataset.

## Running the server
### Prerequisite
- Python 3.7 (Or compatible version)
- PostgreSQL 11.3
Please make sure your environment compatibility before processing.

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. run the server
- Use Django default server for development
```bash
python manage.py runserver
```
- Use `uWSGI` to server
```bash
uwsgi --ini uwsgi.ini
```

Both method will run a server listening `localhost` on port **`8000`**

## Usage
adjast only provides single endpoint `/metrics`. Therefore, to modify the output for this endpoint, you have to attach query parameters. There are several kinds of query parameters:

1. naive data fields
You could basically use every fields listed in the results:
`date`, `channel`, `country`, `os`. Use numerical fields is allowd but not very meaningful. I do not recommend to use it.

Show country is US and os is iPhone:
```bash
http://localhost:8000/metrics?country=US&os=ios
```

2. Time range
`date_from` and `date_to` could help you set start and end point for time. 

Show data from 5/20 ~ 5/25
```bash
http://localhost:8000/metrics?date_from=2017-05-20&date_to=2017-05-25
```

**Note: `date_from` and `date_to` will include the designated date. In the example it will include results on 5/20 and 5/25**

3. sort
`sort` allow all the fields to be the target of ordering.

Sort the result in ascending clicks, descending revenue
```bash
http://localhost:8000/metrics?sort=clicks,-revenue
```

4. aggregate parameters
- `group_by`: Used to indicate on which fields you want to group by. Only allow `date`, `channel`, `country`, `os`. This will return sum results for each aggregated result. If there is no valid fields passed, the results remain untouched.

- `show`: Used together with `group_by`. It indicates what field you want to sum up in the group by. If not passed, it will set to default - all the numerical fields, `impressions`, `clicks`, `installs`, `spend`, `revenue`.

`sort` parameters will become tricky in group by cases. Only those fields in the union of `group_by` and `show` will be functioning. Those sort fields not in the union will be ignored. If there is no valid sort choices, it will be set to the first item in `show`, or `impressions` if there is no `show` parameters.

## Note
This is a demonstrative server, so it is not very strict on the setting principle. `DEBUG = False` indeed, but the `SECRET_KEY` and credentials for database are leave public.