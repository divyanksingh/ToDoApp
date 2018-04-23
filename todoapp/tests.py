from django.test import TestCase
from tastypie.test import TestApiClient
import json
from datetime import date, timedelta


class ToDoAppTestCase(TestCase):
    def setUp(self):

        self.client = TestApiClient()


    def test_task_creation(self):

        due_date = date.today() - timedelta(days=2)
        for i in range(16):

            response = self.client.post('/api/v1/task/', data={
                "title": "test task 1",
                "due_date": due_date,
                "status": "Pending"
                }
            )
            due_date = due_date + timedelta(days=1)
            self.assertEqual(response.status_code, 201)



    def test_today_task_fetch(self):

        self.test_task_creation()
        response = self.client.get('/api/v1/filter/', data={"during":"today"})
        res_obj = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_obj.get('objects')),1)

    def test_this_week_task_fetch(self):

        self.test_task_creation()
        response = self.client.get('/api/v1/filter/', data={"during":"this_week"})
        res_obj = response.json()
        today = date.today()
        start = today
        week_start = today - timedelta(days = today.weekday())
        end = week_start + timedelta(days = 6)
        count = (end - start).days + 1
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_obj.get('objects')),count)

    def test_next_week_task_fetch(self):

        self.test_task_creation()
        response = self.client.get('/api/v1/filter/', data={"during":"next_week"})
        res_obj = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_obj.get('objects')),7)

    def test_overdue_task_fetch(self):

        self.test_task_creation()
        response = self.client.get('/api/v1/filter/', data={"during":"overdue"})
        res_obj = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_obj.get('objects')),2)


    def test_subtask_creation(self):

        self.test_today_task_fetch()
        due_date = date.today()
        response = self.client.post('/api/v1/task/', data={
            "title": "test sub task 1",
            "due_date": due_date,
            "status": "Pending",
            "parent": "/api/v1/task/1/"
            }
        )
        self.assertEqual(response.status_code, 201)


    def test_delete_task(self):
        self.test_subtask_creation()
        response = self.client.put('/api/v1/task/2/', data={
            "deleted": True,
            "deletion_date": date.today()
            })
        self.assertEqual(response.status_code, 204)

   
    def test_fetch_deleted_task(self):
        self.test_delete_task()
        response = self.client.get('/api/v1/deleted/')
        res_obj = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_obj.get('objects')), 1)

