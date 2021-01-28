from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from training_class.models import Client, Group, Exercise, Solution
from training_class.serializers import UserSerializer, ExerciseSerializer, SolutionSerializer


class MyBaseView(APIView):
    permission_classes = [IsAuthenticated]

    def client_status(self, request):
        user_id = auth.get_user(request).id
        status = Client.objects.get(user_id=user_id).status
        return status

    def fidelity_group(self, group_id):
        try:
            Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            return Response({'message': 'неверный запрос группы'}, status=400)

    def fidelity_exercise(self, exercise_id):
        try:
            Exercise.objects.get(id=exercise_id)
        except ObjectDoesNotExist:
            return Response({'message': 'неверный запрос задачи'}, status=400)

    def fidelity_solution(self, solution_id):
        try:
            Exercise.objects.get(id=solution_id)
        except ObjectDoesNotExist:
            return Response({'message': 'неверный запрос ответа'}, status=400)

    def checking_variables(self, *arg):
        list_checking_variables = [self.fidelity_group, self.fidelity_exercise, self.fidelity_solution]
        for i in list(range(len(arg))):
            answer = list_checking_variables[i](arg[i])
            if answer!= None:
                return answer


class TrainingClass(MyBaseView):
    def get(self, request, format=None):
        user_id = auth.get_user(request).id
        client = Client.objects.get(user_id=user_id)
        groups = Group.objects.filter(client=client)
        serializer = UserSerializer(groups, many=True)
        return Response(serializer.data)


class Exercises(MyBaseView):
    def get(self, request, group_id, format=None):
        check = self.checking_variables(group_id)
        if check != None:
            return check
        exercise = Exercise.objects.filter(group_id=group_id)
        serializer = ExerciseSerializer(exercise, many=True, context={'request': request})
        return Response({"exercise": serializer.data})

    def post(self, request, group_id, format=None):
        status = self.client_status(request)
        check = self.checking_variables(group_id)
        if check != None and status != 'teacher':
            return check
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'message': "задача добавлена"}, status=201)


class OneExercise(MyBaseView):
    def get(self, request, group_id, exercise_id, format=None):
        check = self.checking_variables(group_id, exercise_id)
        if check != None:
            return check
        exercise = Exercise.objects.filter(group_id=group_id).filter(id=exercise_id)
        serializer = ExerciseSerializer(exercise, many=True, context={'request': request})
        return Response({"exercise": serializer.data})

    def put(self, request, group_id, exercise_id):
        status = self.client_status(request)
        check = self.checking_variables(group_id, exercise_id)
        if check != None and status != 'teacher':
            return check
        saved_exercise = get_object_or_404(Exercise.objects.all(), id=exercise_id)
        data = request.data.get('exercise')
        serializer = ExerciseSerializer(instance=saved_exercise, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'message': "задача обновлена"}, status=200)

    def delete(self, request, group_id, exercise_id):
        status = self.client_status(request)
        check = self.checking_variables(group_id, exercise_id)
        if check != None and status != 'teacher':
            return check
        article = get_object_or_404(Exercise.objects.all(), id=exercise_id)
        article.delete()
        return Response({'message': "задача удалена"}, status=200)


class Solutions(MyBaseView):
    def get(self, request, group_id, exercise_id, format=None):
        check = self.checking_variables(group_id, exercise_id)
        if check != None:
            return check
        exercise_id = Exercise.objects.filter(id=exercise_id).filter(group_id=group_id)[0].id
        solutions = Solution.objects.filter(exercise_id=exercise_id)
        serializer = SolutionSerializer(solutions, many=True, context={'request': request})
        return Response({"solution": serializer.data})

    def post(self, request, group_id, exercise_id, format=None):
        check = self.checking_variables(group_id, exercise_id)
        status = self.client_status(request)
        if check != None and status != 'student':
            return check
        if Solution.objects.filter(id=auth.get_user(request).id).count() == 0:
            solution = request.data.get("solution")
            serializer = SolutionSerializer(data=solution)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({'message': "ответ добавлен"}, status=201)
        else:
            return Response({'message': "новый ответ создать нельзя, можно изменит существующий"}, status=422)


class OneSolution(MyBaseView):
    def get(self, request, group_id, exercise_id, solution_id, format=None):
        check = self.checking_variables(group_id, exercise_id, solution_id)
        if check != None:
            return check
        exercise_id = Exercise.objects.filter(id=exercise_id).filter(group_id=group_id)[0].id
        solutions = Solution.objects.filter(id=solution_id).filter(exercise_id=exercise_id)
        serializer = SolutionSerializer(solutions, many=True, context={'request': request})
        return Response({"solution": serializer.data})

    def put(self, request, group_id, exercise_id, solution_id, format=None):
        check = self.checking_variables(group_id, exercise_id, solution_id)
        if check != None:
            return check
        saved_solution = get_object_or_404(Solution.objects.all(), id=solution_id)
        data = request.data.get('solution')
        serializer = SolutionSerializer(instance=saved_solution, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'message': "ответ обновлен"}, status=200)
