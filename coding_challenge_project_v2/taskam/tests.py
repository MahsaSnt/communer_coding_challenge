from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Project, Task

User = get_user_model()


class TaskamViewTest(APITestCase):
    URL = '/api/taskam/project/'
    DEVELOPER_ID = 100
    PRODUCT_MANAGER_ID = 101
    PROJECT_1_ID = 100
    PROJECT_2_ID = 101

    def set_up_user(self):
        user1 = User.objects.create(
            id=self.DEVELOPER_ID,
            username='developer',
            role=User.DEVELOPER
        )
        user1.set_password('12345')
        user1.save()

        user2 = User.objects.create(
            id=self.PRODUCT_MANAGER_ID,
            username='product_manager',
            role=User.PRODUCT_MANAGER
        )
        user2.set_password('12345')
        user2.save()

    def obtain_token(self):
        LOGIN_URL = '/api/account/login/'
        response1 = self.client.post(
            LOGIN_URL,
            {
                'username': 'developer',
                'password': '12345'
            }
        )
        self.developer_token = response1.json()['access']

        response2 = self.client.post(
            LOGIN_URL,
            {
                'username': 'product_manager',
                'password': '12345'
            }
        )
        self.product_manager_token = response2.json()['access']

    def set_up_project(self):
        project1 = Project.objects.create(
            id=self.PROJECT_1_ID,
            creator_id=self.PRODUCT_MANAGER_ID,
            title='project1'
        )
        project1.assignees.add(100)
        project2 = Project.objects.create(
            id=self.PROJECT_2_ID,
            creator_id=self.PRODUCT_MANAGER_ID,
            title='project2'
        )

    def set_up_task(self):
        task1 = Task.objects.create(
            id=100,
            creator_id=self.DEVELOPER_ID,
            title='task1',
            project_id=self.PROJECT_1_ID,
        )
        task1.assignees.add(100)

        task2 = Task.objects.create(
            id=101,
            creator_id=self.PRODUCT_MANAGER_ID,
            title='task2',
            project_id=self.PROJECT_1_ID,
        )
        task3 = Task.objects.create(
            id=102,
            creator_id=self.PRODUCT_MANAGER_ID,
            title='task3',
            project_id=self.PROJECT_2_ID,
        )

    def setUp(self) -> None:
        self.set_up_user()
        self.obtain_token()
        self.set_up_project()
        self.set_up_task()

    def test_get_project_unauthorized(self):
        response = self.client.get(
            self.URL,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_project_list(self):
        developer_header = {'HTTP_AUTHORIZATION': f'Bearer {self.developer_token}'}
        response = self.client.get(
            self.URL,
            **developer_header,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        product_manager_header = {'HTTP_AUTHORIZATION': f'Bearer {self.product_manager_token}'}
        response = self.client.get(
            self.URL,
            **product_manager_header,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

    def test_create_project_correct_data(self):
        header = {'HTTP_AUTHORIZATION': f'Bearer {self.product_manager_token}'}
        response = self.client.post(
            self.URL,
            data={
                'title': 'project_title',
                'description': 'project_description',
            },
            **header,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_assign_project_correct_data(self):
        header = {'HTTP_AUTHORIZATION': f'Bearer {self.product_manager_token}'}
        response = self.client.patch(
            self.URL+f'{self.PROJECT_2_ID}/',
            data={
                'assignees_usernames': str(["developer"]).replace("'", '"')
            },
            **header,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_assign_project_by_developer(self):
        header = {'HTTP_AUTHORIZATION': f'Bearer {self.developer_token}'}
        response = self.client.patch(
            self.URL+f'{self.PROJECT_1_ID}/',
            data={
                'assignees_usernames': str(["developer"]).replace("'", '"')
            },
            **header,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_project_wrong_username(self):
        header = {'HTTP_AUTHORIZATION': f'Bearer {self.product_manager_token}'}
        response = self.client.patch(
            self.URL+f'{self.PROJECT_1_ID}/',
            data={
                'assignees_usernames': str(["developer2"]).replace("'", '"')
            },
            **header,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_tasks_of_a_project(self):
        header = {'HTTP_AUTHORIZATION': f'Bearer {self.product_manager_token}'}
        response = self.client.get(
            self.URL+f'{self.PROJECT_1_ID}/task/',
            **header,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

    def test_get_tasks_of_a_developer_in_a_project(self):
        header = {'HTTP_AUTHORIZATION': f'Bearer {self.developer_token}'}
        response = self.client.get(
            self.URL+f'{self.PROJECT_1_ID}/task/'+'?assignees__username=developer',
            **header,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
