To-do Application:

The project is done using Django with Tastypie and AngularJS for frontend.
Celery with redis as broker is used for scheduling the clean-up job on soft deleted tasks older than a month

Steps for usage:

1. Clone the repository and create a virtual environment using python3.
2. Activate the virtual environment and 'pip install -r requirements.txt'
3. python manage.py makemigrations
4. python manage.py migrate
5. redis server should be running on port 6379
6. python manage.py runserver
7. Open http://127.0.0.1:8000/index in browser
8. The worker for clean-up job can be started as 'celery -A todo worker -l info -B'
9. test are written using django.test.TestCase and tastypie.test.TestApiClient







