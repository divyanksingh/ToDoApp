from __future__ import absolute_import, unicode_literals
from celery import task
import requests
from datetime import date, timedelta


@task()
def deletion_task():
	print("here")
	today = date.today()
	check_date = today - timedelta(days=30)
	url = "http://localhost:8000/api/v1/deleted/?deletion_date__lt=" + check_date.strftime('%Y-%m-%d')
	print(url)
	res = requests.delete(url)
	print(res)
