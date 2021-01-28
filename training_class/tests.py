from django.test import Client
from training_class.models import User, Client, Group, Exercise, Solution
from rest_framework.test import APITestCase


class CreateObjectsTest(APITestCase):
    url = None
    request_method = None

    request_data_exercise = {
        "text": "2+2=?",
        "group_id": 1,
        "teacher_id": 2
    }

    request_data_exercise_put = {"exercise": {
        "text": "2-2=?",
        "group_id": 1,
        "teacher_id": 2
    }}

    request_data_solution = {
        "exercise_id": 1,
        "student_id": 1,
        "text": "4",
        "file": "file"
    }

    request_data_solution_put = {"solution": {
        "exercise_id": 1,
        "student_id": 1,
        "text": "10",
        "file": "file2"
    }}

    def setUp(self):
        user1 = User.objects.create(username="user1", password='1q2w3e1q2w3e')
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        student1 = Client.objects.create(user=user1, clientName="Junior",  status="student")
        teacher1 = Client.objects.create(user=user2, clientName="Master", status="teacher")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.client.add(student1)
        group.client.add(teacher1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')
        solution = Solution.objects.create(exercise=exercise, student=student1, text='4', file='file')

    def testGetGroupTrue(self):
        if self.url != None:
            if self.url.find('/groups/1') != -1:
                url = self.url.replace('/groups/1', '/groups/2')
                user2 = User.objects.get(username="user2")
                self.client.force_login(user2)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.data, {"message": "неверный запрос группы"})

    def testGetExerciseTrue(self):
        if self.url != None:
            if self.url.find('/exercises/1') != -1:
                url = self.url.replace('/exercises/1', '/exercises/2')
                user2 = User.objects.get(username="user2")
                self.client.force_login(user2)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.data,  {"message": "неверный запрос задачи"})

    def testGetSolutionTrue(self):
        if self.url != None:
            if self.url.find('/solutions/1') != -1:
                url = self.url.replace('/solutions/1', '/solutions/11')
                user2 = User.objects.get(username="user2")
                self.client.force_login(user2)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.data, {"message": "неверный запрос ответа"})

    def testUnauthorized(self):
        expected_response_data = {
            "detail": "Учетные данные не были предоставлены."
        }
        list_method_auth = {'get': self.client.get, 'post': self.client.post, 'put': self.client.put, 'delete': self.client.delete}
        if self.url != None:
            for key in list_method_auth:
                if key in self.request_method:
                    response = list_method_auth[key](self.url)
                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(response.data, expected_response_data)


class TrainingClassTest(CreateObjectsTest):
    url = '/education/groups'
    request_method = ['get']

    def testGetTeacherGroups(self):
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": 1, "groupName": "Group"}])

    def testGetStudentGroups(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": 1, "groupName": "Group"}])


class ExercisesTest(CreateObjectsTest):
    url = '/education/groups/1/exercises'
    request_method = ['get', 'post']

    def testGetTeacherExercises(self):
        user2 = User.objects.get(username="user2")
        response_data = {"exercise": [self.request_data_exercise]}
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def testAddTeacherExercises(self):
        user2 = User.objects.get(username="user2")
        response_data = self.request_data_exercise
        self.client.force_login(user2)
        response = self.client.post(self.url, response_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"message": "задача добавлена"})

    def testGetStudentExercises(self):
        user1 = User.objects.get(username="user1")
        response_data = self.request_data_exercise
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"exercise": [response_data]})


class ExerciseTest(CreateObjectsTest):
    url = '/education/groups/1/exercises/1'
    request_method = ['get', 'put', 'delete']

    def testGetTeacherExercise(self):
        user2 = User.objects.get(username="user2")
        response_data = {'exercise': [self.request_data_exercise]}
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def testGetStudentExercise(self):
        user1 = User.objects.get(username="user1")
        response_data = {'exercise': [self.request_data_exercise]}
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def testPutExercise(self):
        user2 = User.objects.get(username="user2")
        response_data = self.request_data_exercise_put
        self.client.force_login(user2)
        response = self.client.put(self.url, response_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "задача обновлена"})

    def testDeleteExercise(self):
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "задача удалена"})


class TeacherSolutionsTest(CreateObjectsTest):
    url = '/education/groups/1/exercises/1/solutions'
    request_method = ['get', 'post']

    def testGetTeacherSolutions(self):
        user2 = User.objects.get(username="user2")
        response_data = {"solution": [self.request_data_solution]}
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def testGetStudentSolutions(self):
        user1 = User.objects.get(username="user1")
        response_data = {"solution": [self.request_data_solution]}
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def testAddStudentSolutions(self):
        Solution.objects.filter(id=1).delete()
        user1 = User.objects.get(username="user1")
        response_data = {"solution": self.request_data_solution}
        self.client.force_login(user1)
        response = self.client.post(self.url, response_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data,  {"message": "ответ добавлен"})

    def testAddNewStudentSolutions(self):
        user1 = User.objects.get(username="user1")
        response_data = {"solution": self.request_data_solution}
        self.client.force_login(user1)
        response = self.client.post(self.url, response_data, format='json')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {"message": "новый ответ создать нельзя, можно изменит существующий"})


class TeacherSolutionTest(CreateObjectsTest):
    url = '/education/groups/1/exercises/1/solutions/1'
    request_method = ['get', 'put', 'delete']

    def testGetTeacherSolution(self):
        user2 = User.objects.get(username="user2")
        response_data = {'solution': [self.request_data_solution]}
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def testPutTeacherSolution(self):
        user2 = User.objects.get(username="user2")
        response_data = self.request_data_solution_put
        self.client.force_login(user2)
        response = self.client.put(self.url, response_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "ответ обновлен"})

    def testGetStudentSolution(self):
        user1 = User.objects.get(username="user1")
        response_data = {'solution': [self.request_data_solution]}
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def testPutStudentSolution(self):
        user1 = User.objects.get(username="user1")
        response_data = self.request_data_solution_put
        self.client.force_login(user1)
        response = self.client.put(self.url, response_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "ответ обновлен"})

