from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from training_class.models import Client, Group, Exercise, Solution
#from training_class.permissions import IsUser
from training_class.serializers import UserSerializer, ExerciseSerializer, SolutionSerializer


class BaseView(APIView):
    permission_classes = [IsAuthenticated]

    def auth_client(self, request):
        try:
            user = auth.get_user(request)
            Client.objects.get(user_id=user.id)
        except ObjectDoesNotExist:
            return Response('авторизуйтесь', status=401)

    def client_status(self, request):
        user_id = auth.get_user(request).id
        status = Client.objects.get(user_id=user_id).status
        return status

    def fidelity_group(self, group_id):
        try:
            Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            return Response('неверный запрос группы', status=400)

    def fidelity_exercise(self, exercise_id):
        try:
            Exercise.objects.get(id=exercise_id)
        except ObjectDoesNotExist:
            return Response('неверный запрос задачи', status=400)

    def fidelity_solution(self, solution_id):
        try:
            Exercise.objects.get(id=solution_id)
        except ObjectDoesNotExist:
            return Response('неверный запрос ответа', status=400)


class TrainingClass(BaseView):
    def get(self, request, format=None):
        answer_auth = self.auth_client(request)
        if answer_auth != None:
            return answer_auth
        else:
            user_id = auth.get_user(request).id
            client = Client.objects.get(user_id=user_id)
            groups = Group.objects.filter(client=client)
            serializer = UserSerializer(groups, many=True)
            return Response(serializer.data)


class Exercises(BaseView):
    def get(self, request, group_id, format=None):
        answer_auth = self.auth_client(request)
        if answer_auth != None:
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        exercise = Exercise.objects.filter(group_id=group_id)
        serializer = ExerciseSerializer(exercise, many=True, context={'request': request})
        return Response({"exercise": serializer.data})

    def post(self, request, group_id, format=None):
        answer_auth = self.auth_client(request)
        status = self.client_status(request)
        if answer_auth != None or status != 'teacher':
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response("задача добавлена", status=201)


class OneExercise(BaseView):
    def get(self, request, group_id, exercise_id, format=None):
        answer_auth = self.auth_client(request)
        if answer_auth!=None:
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        answer_exercise = self.fidelity_exercise(exercise_id)
        if answer_exercise != None:
            return answer_exercise
        exercise = Exercise.objects.filter(group_id=group_id).filter(id=exercise_id)
        serializer = ExerciseSerializer(exercise, many=True, context={'request': request})
        return Response({"exercise": serializer.data})

    def put(self, request, group_id, exercise_id):
        answer_auth = self.auth_client(request)
        status = self.client_status(request)
        if answer_auth != None or status != 'teacher':
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        answer_exercise = self.fidelity_exercise(exercise_id)
        if answer_exercise != None:
            return answer_exercise
        saved_exercise = get_object_or_404(Exercise.objects.all(), id=exercise_id)
        data = request.data.get('exercise')
        serializer = ExerciseSerializer(instance=saved_exercise, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response("задача обновлена", status=200)

    def delete(self, request, group_id, exercise_id):
        answer_auth = self.auth_client(request)
        status = self.client_status(request)
        if answer_auth!=None or status != 'teacher':
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        answer_exercise = self.fidelity_exercise(exercise_id)
        if answer_exercise != None:
            return answer_exercise
        article = get_object_or_404(Exercise.objects.all(), id=exercise_id)
        article.delete()
        return Response("задача удалена", status=200)


class Solutions(BaseView):
    def get(self, request, group_id, exercise_id, format=None):
        answer_auth = self.auth_client(request)
        if answer_auth!=None:
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        answer_exercise = self.fidelity_exercise(exercise_id)
        if answer_exercise != None:
            return answer_exercise
        exercise_id = Exercise.objects.filter(id=exercise_id).filter(group_id=group_id)[0].id
        solutions = Solution.objects.filter(exercise_id=exercise_id)
        serializer = SolutionSerializer(solutions, many=True, context={'request': request})
        return Response({"solution": serializer.data})

    def post(self, request, group_id, exercise_id, format=None):
        answer_auth = self.auth_client(request)
        if answer_auth!=None != 'student':
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        answer_exercise = self.fidelity_exercise(exercise_id)
        if answer_exercise != None:
            return answer_exercise
        if Solution.objects.filter(id=auth.get_user(request).id).count() == 0:
            solution = request.data.get("solution")
            serializer = SolutionSerializer(data=solution)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response("ответ добавлен", status=201)
        else:
            return Response("новый ответ создать нельзя, можно изменит существующий", status=422)


class OneSolution(BaseView):
    def get(self, request, group_id, exercise_id, solution_id, format=None):
        answer_auth = self.auth_client(request)
        if answer_auth!=None:
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        answer_exercise = self.fidelity_exercise(exercise_id)
        if answer_exercise != None:
            return answer_exercise
        answer_solution = self.fidelity_solution(solution_id)
        if answer_solution != None:
            return answer_solution
        exercise_id = Exercise.objects.filter(id=exercise_id).filter(group_id=group_id)[0].id
        solutions = Solution.objects.filter(id=solution_id).filter(exercise_id=exercise_id)
        serializer = SolutionSerializer(solutions, many=True, context={'request': request})
        return Response({"solution": serializer.data})

    def put(self, request, group_id, exercise_id, solution_id, format=None):
        answer_auth = self.auth_client(request)
        if answer_auth!=None:
            return answer_auth
        answer_group = self.fidelity_group(group_id)
        if answer_group != None:
            return answer_group
        answer_exercise = self.fidelity_exercise(exercise_id)
        if answer_exercise != None:
            return answer_exercise
        answer_solution = self.fidelity_solution(solution_id)
        if answer_solution != None:
            return answer_solution
        saved_solution = get_object_or_404(Solution.objects.all(), id=solution_id)
        data = request.data.get('solution')
        serializer = SolutionSerializer(instance=saved_solution, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response("ответ обновлен", status=200)
