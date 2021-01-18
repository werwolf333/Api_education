from rest_framework.test import APIRequestFactory
from django.test import Client
from training_class import views
from training_class.models import User, Teacher, Student, Group, Exercise, Solution
from rest_framework.test import APITestCase
from rest_framework import status
from training_class.serializers import UserSerializer


class TeacherTrainingClassTest(APITestCase):
    url = '/education/teacher-api/groups'

    def setUp(self):
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        teacher1 = Teacher.objects.create(user=user2, teacherName="Junior")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.teacher.add(teacher1)

    def testGetTeacherGroups(self):
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": 1, "groupName": "Group"}])

    def testGetUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)


class TeacherExercisesTest(APITestCase):
    url = '/education/teacher-api/groups/1/exercises'

    def setUp(self):
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        teacher1 = Teacher.objects.create(user=user2, teacherName="Junior")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.teacher.add(teacher1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')

    def testGetTeacherExercises(self):
        user2 = User.objects.get(username="user2")
        expected_response_data = {"exercise": [{
            "text": "2+2=?",
            "group_id": 1,
            "teacher_id": 1
        }]}
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response_data)

    def testAddTeacherExercises(self):
        user2 = User.objects.get(username="user2")
        request_data = {
            "text": "2+2=?",
            "group_id": 1,
            "teacher_id": 1
        }
        self.client.force_login(user2)
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, "задача добавлена")

    def testGetGroupTrue(self):
        url = '/education/teacher-api/groups/2/exercises'
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос группы")

    def testGetUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)

    def testPostUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)


class TeacherExerciseTest(APITestCase):
    url = '/education/teacher-api/groups/1/exercises/1'

    def setUp(self):
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        teacher1 = Teacher.objects.create(user=user2, teacherName="Junior")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.teacher.add(teacher1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')

    def testGetTeacherExercise(self):
        user2 = User.objects.get(username="user2")
        expected_response_data = {"exercise": [{
            "text": "2+2=?",
            "group_id": 1,
            "teacher_id": 1
        }]}
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response_data)

    def testPutTeacherExercise(self):
        user2 = User.objects.get(username="user2")
        request_data = {"exercise": {
            "text": "2-2=?",
            "group_id": 1,
            "teacher_id": 1
        }}
        self.client.force_login(user2)
        response = self.client.put(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "задача обновлена")

    def testDeleteTeacherExercise(self):
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "задача удалена")

    def testGetGroupTrue(self):
        url = '/education/teacher-api/groups/2/exercises/1'
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос группы")

    def testGetExerciseTrue(self):
        url = '/education/teacher-api/groups/1/exercises/2'
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос задачи")

    def testGetUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)

    def testPutUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)

    def testDeleteUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)


class TeacherSolutionsTest(APITestCase):
    url = '/education/teacher-api/groups/1/exercises/1/solutions'

    def setUp(self):
        user1 = User.objects.create(username="user1", password='1q2w3e1q2w3e')
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        teacher1 = Teacher.objects.create(user=user2, teacherName="Junior")
        student1 = Student.objects.create(user=user1, studentName="Junior")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.student.add(student1)
        group.teacher.add(teacher1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')
        solution = Solution.objects.create(exercise=exercise, student=student1, text='4', file='file')

    def testGetTeacherSolutions(self):
        user2 = User.objects.get(username="user2")
        request_data = {"solution": [{
            "exercise_id": 1,
            "student_id": 1,
            "text": "4",
            "file": "file"
        }]}
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, request_data)

    def testGetGroupTrue(self):
        url = '/education/teacher-api/groups/2/exercises/1/solutions'
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос группы")

    def testGetExerciseTrue(self):
        url = '/education/teacher-api/groups/1/exercises/2/solutions'
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос задачи")

    def testGetUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)


class TeacherSolutionTest(APITestCase):
    url = '/education/teacher-api/groups/1/exercises/1/solutions/1'

    def setUp(self):
        user1 = User.objects.create(username="user1", password='1q2w3e1q2w3e')
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        teacher1 = Teacher.objects.create(user=user2, teacherName="Junior")
        student1 = Student.objects.create(user=user1, studentName="Junior")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.student.add(student1)
        group.teacher.add(teacher1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')
        solution = Solution.objects.create(exercise=exercise, student=student1, text='4', file='file')

    def testGetTeacherSolution(self):
        user2 = User.objects.get(username="user2")
        request_data = {"solution": [{
            "exercise_id": 1,
            "student_id": 1,
            "text": "4",
            "file": "file"
        }]}
        self.client.force_login(user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, request_data)

    def testPutStudentSolution(self):
        user2 = User.objects.get(username="user2")
        request_data = {"solution": {
            "exercise_id": 1,
            "student_id": 1,
            "text": "10",
            "file": "file2"
        }}
        self.client.force_login(user2)
        response = self.client.put(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "ответ обновлен")

    def testGetGroupTrue(self):
        url = '/education/teacher-api/groups/2/exercises/1/solutions/1'
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос группы")

    def testGetExerciseTrue(self):
        url = '/education/teacher-api/groups/1/exercises/2/solutions/1'
        user2 = User.objects.get(username="user2")
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос задачи")

    def testGetUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)

    def testPutUnauthorizedTeacherExercises(self):
        expected_response_data = 'авторизуйтесь как учитель'
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)

#--------------------------------------------------------------


class StudentTrainingClassTest(APITestCase):
    url = '/education/student-api/groups'

    def setUp(self):
        user1 = User.objects.create(username="user1", password='1q2w3e1q2w3e')
        student1 = Student.objects.create(user=user1, studentName="Junior")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.student.add(student1)

    def testGetStudentGroups(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": 1, "groupName": "Group"}])

    def testGetUnauthorizedStudentExercises(self):
        expected_response_data = 'авторизуйтесь как ученик'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)


class StudentExercisesTest(APITestCase):

    url = '/education/student-api/groups/1/exercises'

    def setUp(self):
        user1 = User.objects.create(username="user1", password='1q2w3e1q2w3e')
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        student1 = Student.objects.create(user=user1, studentName="Junior")
        teacher1 = Teacher.objects.create(user=user2, teacherName="Master")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.student.add(student1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')

    def testGetStudentExercises(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"exercise": [{
            "text": "2+2=?",
            "group_id": 1,
            "teacher_id": 1
        }]})

    def testGetGroupTrue(self):
        url = '/education/student-api/groups/2/exercises'
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос группы")

    def testGetUnauthorizedStudentExercises(self):
        expected_response_data = 'авторизуйтесь как ученик'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)


class StudentExerciseTest(APITestCase):

    url = '/education/student-api/groups/1/exercises/1'

    def setUp(self):
        user1 = User.objects.create(username="user1", password='1q2w3e1q2w3e')
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        student1 = Student.objects.create(user=user1, studentName="Junior")
        teacher1 = Teacher.objects.create(user=user2, teacherName="Master")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.student.add(student1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')

    def testGetStudentExercise(self):
        user1 = User.objects.get(username="user1")
        expected_response_data = {"exercise": [{
            "text": "2+2=?",
            "group_id": 1,
            "teacher_id": 1
        }]}
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response_data)

    def testGetGroupTrue(self):
        url = '/education/student-api/groups/2/exercises/1'
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос группы")

    def testGetExerciseTrue(self):
        url = '/education/student-api/groups/1/exercises/2'
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос задачи")

    def testGetUnauthorizedStudentExercises(self):
        expected_response_data = 'авторизуйтесь как ученик'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)


class StudentSolutionsTest(APITestCase):
    url = '/education/student-api/groups/1/exercises/1/solutions'

    def setUp(self):
        user1 = User.objects.create(username="user1", password='1q2w3e1q2w3e')
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        student1 = Student.objects.create(user=user1, studentName="Junior")
        teacher1 = Teacher.objects.create(user=user2, teacherName="Master")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.student.add(student1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')

    def testGetStudentSolutions(self):
        self.testAddStudentSolutions()
        user1 = User.objects.get(username="user1")
        request_data = {"solution": [{
            "exercise_id": 1,
            "student_id": 1,
            "text": "4",
            "file": "file"
        }]}
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, request_data)

    def testAddStudentSolutions(self):
        user1 = User.objects.get(username="user1")
        request_data = {"solution": {
            "exercise_id": 1,
            "student_id": 1,
            "text": "4",
            "file": "file"
        }}
        self.client.force_login(user1)
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, "ответ добавлен")

    def testAddNewStudentSolutions(self):
        self.testAddStudentSolutions()
        user1 = User.objects.get(username="user1")
        request_data = {"solution": {
            "exercise_id": 1,
            "student_id": 1,
            "text": "4",
            "file": "file"
        }}
        self.client.force_login(user1)
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "новый ответ создать нельзя, можно изменит существующий")

    def testGetGroupTrue(self):
        url = '/education/student-api/groups/2/exercises/1/solutions'
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос группы")

    def testGetExerciseTrue(self):
        url = '/education/student-api/groups/1/exercises/2/solutions'
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос задачи")

    def testGetUnauthorizedStudentExercises(self):
        expected_response_data = 'авторизуйтесь как ученик'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)

    def testPostUnauthorizedStudentExercises(self):
        expected_response_data = 'авторизуйтесь как ученик'
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)


class StudentSolutionTest(APITestCase):
    url = '/education/student-api/groups/1/exercises/1/solutions/1'

    def setUp(self):
        user1 = User.objects.create(username="user1", password='1q2w3e1q2w3e')
        user2 = User.objects.create(username="user2", password='1q2w3e1q2w3e')
        student1 = Student.objects.create(user=user1, studentName="Junior")
        teacher1 = Teacher.objects.create(user=user2, teacherName="Master")
        group = Group.objects.create(groupName='Group')
        group.save()
        group.student.add(student1)
        exercise = Exercise.objects.create(group=group, teacher=teacher1, text='2+2=?')
        solution = Solution.objects.create(exercise=exercise, student=student1, text='4', file='file')

    def testGetStudentSolution(self):
        user1 = User.objects.get(username="user1")
        request_data = {"solution": [{
            "exercise_id": 1,
            "student_id": 1,
            "text": "4",
            "file": "file"
        }]}
        self.client.force_login(user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, request_data)

    def testPutStudentSolution(self):
        user1 = User.objects.get(username="user1")
        request_data = {"solution": {
            "exercise_id": 1,
            "student_id": 1,
            "text": "10",
            "file": "file2"
        }}
        self.client.force_login(user1)
        response = self.client.put(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "ответ обновлен")

    def testGetGroupTrue(self):
        url = '/education/student-api/groups/2/exercises/1/solutions'
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос группы")

    def testGetExerciseTrue(self):
        url = '/education/student-api/groups/1/exercises/2/solutions/1'
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "неверный запрос задачи")

    def testGetUnauthorizedStudentExercises(self):
        expected_response_data = 'авторизуйтесь как ученик'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)

    def testPutUnauthorizedStudentExercises(self):
        expected_response_data = 'авторизуйтесь как ученик'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)
