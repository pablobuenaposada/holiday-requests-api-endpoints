## Setup (needs Docker)
To have the project running you need to execute the following commands:
```bash
make docker/build
make docker/run
```
After this the project should be running in a container and the API should be exposed through http://localhost:8000/api/

The image would also create 2 users, one manager and one worker, check the docker logs (following example) to get respective tokens.

If you want to create additional users or tokens use `createsuperuser` and `drf_create_token` django-admin commands.
```
PYTHONPATH=src venv/bin/python src/manage.py createsuperuser --noinput --username user_manager --type manager

Superuser created successfully.

PYTHONPATH=src venv/bin/python src/manage.py createsuperuser --noinput --username user_worker --type worker

Superuser created successfully.

PYTHONPATH=src venv/bin/python src/manage.py drf_create_token user_manager

Generated token 5a8e89b2197ee1200f77a6cc0563ea209670b43e for user user_manager

PYTHONPATH=src venv/bin/python src/manage.py drf_create_token user_worker

Generated token 54c6893fd726514c9463f0b523e86577d2b38bac for user user_worker

PYTHONPATH=src venv/bin/python src/manage.py runserver 0.0.0.0:8000

Watching for file changes with StatReloader

Search...
Stick to bottom
```

## Running the tests
As easy as:
```bash
make docker/tests
```
Example output:
```
(venv) pablobuenaposadasanchez@Pablos-MacBook-Pro holiday-requests-api-endpoints-qrfbyi % make docker/tests
docker run holidays /bin/sh -c 'make tests'
venv/bin/pip install -r requirements-tests.txt
Collecting black
  Downloading black-22.10.0-py3-none-any.whl (165 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 165.8/165.8 KB 3.7 MB/s eta 0:00:00
Collecting isort
  Downloading isort-5.10.1-py3-none-any.whl (103 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 103.4/103.4 KB 13.9 MB/s eta 0:00:00
Collecting flake8
  Downloading flake8-6.0.0-py2.py3-none-any.whl (57 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.8/57.8 KB 8.4 MB/s eta 0:00:00
Collecting pytest
  Downloading pytest-7.2.0-py3-none-any.whl (316 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 316.8/316.8 KB 16.2 MB/s eta 0:00:00
Collecting pytest-django
  Downloading pytest_django-4.5.2-py3-none-any.whl (20 kB)
Collecting model-bakery
  Downloading model_bakery-1.9.0-py2.py3-none-any.whl (22 kB)
Collecting pathspec>=0.9.0
  Downloading pathspec-0.10.2-py3-none-any.whl (28 kB)
Collecting platformdirs>=2
  Downloading platformdirs-2.5.4-py3-none-any.whl (14 kB)
Collecting mypy-extensions>=0.4.3
  Downloading mypy_extensions-0.4.3-py2.py3-none-any.whl (4.5 kB)
Collecting tomli>=1.1.0
  Downloading tomli-2.0.1-py3-none-any.whl (12 kB)
Collecting click>=8.0.0
  Downloading click-8.1.3-py3-none-any.whl (96 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 96.6/96.6 KB 18.3 MB/s eta 0:00:00
Collecting pyflakes<3.1.0,>=3.0.0
  Downloading pyflakes-3.0.1-py2.py3-none-any.whl (62 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.8/62.8 KB 19.3 MB/s eta 0:00:00
Collecting mccabe<0.8.0,>=0.7.0
  Downloading mccabe-0.7.0-py2.py3-none-any.whl (7.3 kB)
Collecting pycodestyle<2.11.0,>=2.10.0
  Downloading pycodestyle-2.10.0-py2.py3-none-any.whl (41 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 41.3/41.3 KB 11.8 MB/s eta 0:00:00
Collecting iniconfig
  Downloading iniconfig-1.1.1-py2.py3-none-any.whl (5.0 kB)
Collecting packaging
  Downloading packaging-21.3-py3-none-any.whl (40 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 40.8/40.8 KB 14.6 MB/s eta 0:00:00
Collecting exceptiongroup>=1.0.0rc8
  Downloading exceptiongroup-1.0.4-py3-none-any.whl (14 kB)
Collecting pluggy<2.0,>=0.12
  Downloading pluggy-1.0.0-py2.py3-none-any.whl (13 kB)
Collecting attrs>=19.2.0
  Downloading attrs-22.1.0-py2.py3-none-any.whl (58 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 58.8/58.8 KB 15.6 MB/s eta 0:00:00
Requirement already satisfied: django>=3.2 in ./venv/lib/python3.10/site-packages (from model-bakery->-r requirements-tests.txt (line 6)) (4.1)
Requirement already satisfied: asgiref<4,>=3.5.2 in ./venv/lib/python3.10/site-packages (from django>=3.2->model-bakery->-r requirements-tests.txt (line 6)) (3.5.2)
Requirement already satisfied: sqlparse>=0.2.2 in ./venv/lib/python3.10/site-packages (from django>=3.2->model-bakery->-r requirements-tests.txt (line 6)) (0.4.3)
Collecting pyparsing!=3.0.5,>=2.0.2
  Downloading pyparsing-3.0.9-py3-none-any.whl (98 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 98.3/98.3 KB 25.4 MB/s eta 0:00:00
Installing collected packages: mypy-extensions, iniconfig, tomli, pyparsing, pyflakes, pycodestyle, pluggy, platformdirs, pathspec, mccabe, isort, exceptiongroup, click, attrs, packaging, model-bakery, flake8, black, pytest, pytest-django
Successfully installed attrs-22.1.0 black-22.10.0 click-8.1.3 exceptiongroup-1.0.4 flake8-6.0.0 iniconfig-1.1.1 isort-5.10.1 mccabe-0.7.0 model-bakery-1.9.0 mypy-extensions-0.4.3 packaging-21.3 pathspec-0.10.2 platformdirs-2.5.4 pluggy-1.0.0 pycodestyle-2.10.0 pyflakes-3.0.1 pyparsing-3.0.9 pytest-7.2.0 pytest-django-4.5.2 tomli-2.0.1
WARNING: You are using pip version 22.0.4; however, version 22.3.1 is available.
You should consider upgrading via the '/app/venv/bin/python3.10 -m pip install --upgrade pip' command.
DJANGO_SETTINGS_MODULE=main.settings PYTHONPATH=src venv/bin/pytest src/tests
============================= test session starts ==============================
platform linux -- Python 3.10.4, pytest-7.2.0, pluggy-1.0.0
django: settings: main.settings (from env)
rootdir: /app
plugins: django-4.5.2
collected 49 items

src/tests/api/remaining/test_views.py ..                                 [  4%]
src/tests/api/requests/test_serializers.py .                             [  6%]
src/tests/api/requests/test_views.py .............                       [ 32%]
src/tests/api/requests/overlaps/test_serializers.py .                    [ 34%]
src/tests/api/requests/overlaps/test_views.py ...                        [ 40%]
src/tests/request/test_domain.py ....................                    [ 81%]
src/tests/request/test_models.py ....                                    [ 89%]
src/tests/api/remaining/test_serializers.py .                            [ 91%]
src/tests/api/requests/test_serializers.py ....                          [100%]

============================== 49 passed in 0.32s ==============================
```

## Endpoints
All the endpoints are under token authentication, check the examples to see how the token is passed through the headers.
Depending on the token used, the application will detect if you are a manager or a worker so the behaviour of the endpoint will act accordingly.

### Retrieve requests  - `GET http://localhost:8000/api/requests/`
Depending on the token used the requests retrieved may differ, if worker token is used only its own requests would be returned,
if manager token is used all requests would be returned.
In this example manager token is used.
```bash
curl --request GET \
  --url http://localhost:8000/api/requests/ \
  --header 'Authorization: Token 5a8e89b2197ee1200f77a6cc0563ea209670b43e'

{
	"count": 3,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"author": 1,
			"status": "approved",
			"resolved_by": 1,
			"request_created_at": "2022-11-27T23:50:05.207897Z",
			"vacation_start_date": "2022-01-01",
			"vacation_end_date": "2022-01-02"
		},
		{
			"id": 2,
			"author": 2,
			"status": "approved",
			"resolved_by": 1,
			"request_created_at": "2022-11-27T23:50:27.048376Z",
			"vacation_start_date": "2022-01-01",
			"vacation_end_date": "2022-01-02"
		},
		{
			"id": 3,
			"author": 2,
			"status": "pending",
			"resolved_by": null,
			"request_created_at": "2022-11-27T23:56:42.177255Z",
			"vacation_start_date": "2022-01-02",
			"vacation_end_date": "2022-01-03"
		}
	]
}
```

### Filter requests by status - `GET http://localhost:8000/api/requests/?status={approved, pending, rejected}`
Can be used for managers and workers tokens.
````bash
curl --request GET \
  --url 'http://localhost:8000/api/requests/?status=approved' \
  --header 'Authorization: Token 54c6893fd726514c9463f0b523e86577d2b38bac'

{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 2,
			"author": 2,
			"status": "approved",
			"resolved_by": 1,
			"request_created_at": "2022-11-27T23:50:27.048376Z",
			"vacation_start_date": "2022-01-01",
			"vacation_end_date": "2022-01-02"
		}
	]
}
````

### Filter requests by author - `GET http://localhost:8000/api/requests/?author=2`
This only makes sense to use it with managers but if you use it with a worker nothing will complain.
```bash
curl --request GET \
  --url 'http://localhost:8000/api/requests/?author=2' \
  --header 'Authorization: Token 5a8e89b2197ee1200f77a6cc0563ea209670b43e'

{
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 2,
			"author": 2,
			"status": "approved",
			"resolved_by": 1,
			"request_created_at": "2022-11-27T23:50:27.048376Z",
			"vacation_start_date": "2022-01-01",
			"vacation_end_date": "2022-01-02"
		},
		{
			"id": 3,
			"author": 2,
			"status": "pending",
			"resolved_by": null,
			"request_created_at": "2022-11-27T23:56:42.177255Z",
			"vacation_start_date": "2022-01-02",
			"vacation_end_date": "2022-01-03"
		}
	]
}
```

### See own remaining days - `GET http://localhost:8000/api/remaining/`
Can be used with workers and managers (yes, managers are also allowed to have holidays), each of them will retrieve their own days left. 
```bash
curl --request GET \
  --url http://localhost:8000/api/remaining/ \
  --header 'Authorization: Token 54c6893fd726514c9463f0b523e86577d2b38bac'

{
	"days": 29
}
```

### New request - `POST http://localhost:8000/api/requests/`
Can be used with managers and workers.

You only need to supply `vacation_start_date` and `vacation_end_date`.

If start date is greater than end date it will throw `400-Bad request` with message `vacation_start_date should be earlier than vacation_end_date`.

If there's not enough days left for the particular request it will throw `409-Conflict` with message `This request overlaps with an existing one`.

If there's a request that overlaps with the one that is getting created it will throw `409-Conflict` with message `This request overlaps with an existing one`.
```bash
curl --request POST \
  --url http://localhost:8000/api/requests/ \
  --header 'Authorization: Token 54c6893fd726514c9463f0b523e86577d2b38bac' \
  --header 'Content-Type: application/json' \
  --data '{"vacation_start_date": "2022-1-1", "vacation_end_date": "2022-1-2"}'

{
	"id": 2,
	"author": 2,
	"status": "pending",
	"resolved_by": null,
	"request_created_at": "2022-11-27T23:50:27.048376Z",
	"vacation_start_date": "2022-01-01",
	"vacation_end_date": "2022-01-02"
} 
```

### See overlapping requests - `GET http://localhost:8000/api/requests/overlaps/`
Only for managers, if used with a worker it will return 403-Forbidden.

Returns a list of pending requests that have an overlap with others (pending or approved), this is represented by the field `overlaps` 
which represents a list of the other requests that matches totally or partially the parent request.

In this example request 3 and 4 overlap between them, so each one is returned in the main list and then the `overlaps` field will contain the "opposite" request.
```bash
curl --request GET \
  --url http://localhost:8000/api/requests/overlaps/ \
  --header 'Authorization: Token 5a8e89b2197ee1200f77a6cc0563ea209670b43e'

{
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 3,
			"overlaps": [
				{
					"id": 4,
					"author": 1,
					"status": "pending",
					"resolved_by": null,
					"request_created_at": "2022-11-28T00:15:08.069054Z",
					"vacation_start_date": "2022-01-02",
					"vacation_end_date": "2022-01-03"
				}
			],
			"vacation_start_date": "2022-01-02",
			"vacation_end_date": "2022-01-03"
		},
		{
			"id": 4,
			"overlaps": [
				{
					"id": 3,
					"author": 2,
					"status": "pending",
					"resolved_by": null,
					"request_created_at": "2022-11-27T23:56:42.177255Z",
					"vacation_start_date": "2022-01-02",
					"vacation_end_date": "2022-01-03"
				}
			],
			"vacation_start_date": "2022-01-02",
			"vacation_end_date": "2022-01-03"
		}
	]
}
```

### Approve or reject requests - `PATCH http://localhost:8000/api/requests/2/`
Only for managers, if used with a worker it will return 403-Forbidden.

You can only play with the `status` field and only with values `approved` and `rejected`.
```bash
curl --request PATCH \
  --url http://localhost:8000/api/requests/2/ \
  --header 'Authorization: Token 5a8e89b2197ee1200f77a6cc0563ea209670b43e' \
  --header 'Content-Type: application/json' \
  --data '{
	"status": "approved"
}'

{
	"id": 2,
	"author": 2,
	"status": "approved",
	"resolved_by": 1,
	"request_created_at": "2022-11-27T23:50:27.048376Z",
	"vacation_start_date": "2022-01-01",
	"vacation_end_date": "2022-01-02"
}
```