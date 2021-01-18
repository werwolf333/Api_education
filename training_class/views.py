from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from training_class.models import Teacher, Student, Group, Exercise, Solution
from training_class.serializers import UserSerializer, ExerciseSerializer, SolutionSerializer


def authTeacher(request):
    user = auth.get_user(request)
    try:
        teacher = Teacher.objects.get(user_id=user.id)
    except ObjectDoesNotExist:
        return Response('авторизуйтесь как учитель', status=401)


def authStudent(request):
    user = auth.get_user(request)
    try:
        teacher = Student.objects.get(user_id=user.id)
    except ObjectDoesNotExist:
        return Response('авторизуйтесь как ученик', status=401)


def fidelityGroup(group_id):
    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response('неверный запрос группы', status=400)


def fidelityExercise(exercise_id):
    try:
        exercise = Exercise.objects.get(id=exercise_id)
    except ObjectDoesNotExist:
        return Response('неверный запрос задачи', status=400)

def fidelitySolution(solution_id):
    try:
        solution = Exercise.objects.get(id=solution_id)
    except ObjectDoesNotExist:
        return Response('неверный запрос ответа', status=400)


class TeacherTrainingClass(APIView):
    def get(self, request, format=None):
        answerAuth = authTeacher(request)
        if answerAuth!=None:
            return answerAuth
        else:
            user_id = auth.get_user(request).id
            teacher = Teacher.objects.get(user_id=user_id)
            groups = Group.objects.filter(teacher=teacher)
            serializer = UserSerializer(groups, many=True)
            return Response(serializer.data)


class TeacherExercises(APIView):
    def get(self, request, group_id, format=None):
        answerAuth = authTeacher(request)
        answerGroup = fidelityGroup(group_id)
        if answerAuth!=None:
            return answerAuth
        elif answerGroup != None:
            return answerGroup
        else:
            exercise = Exercise.objects.filter(group_id=group_id)
            serializer = ExerciseSerializer(exercise, many=True, context={'request': request})
            return Response({"exercise": serializer.data})

    def post(self, request, group_id, format=None):
        answerAuth = authTeacher(request)
        if answerAuth!=None:
            return answerAuth
        else:
            serializer = ExerciseSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response("задача добавлена", status=201)


class TeacherExercise(APIView):
    def get(self, request, group_id, exercise_id, format=None):
        answerAuth = authTeacher(request)
        answerGroup = fidelityGroup(group_id)
        answerExercise = fidelityExercise(exercise_id)
        if answerAuth!=None:
            return answerAuth
        elif answerGroup != None:
            return answerGroup
        elif answerExercise != None:
            return answerExercise
        else:
            exercise = Exercise.objects.filter(group_id=group_id).filter(id=exercise_id)
            serializer = ExerciseSerializer(exercise, many=True, context={'request': request})
            return Response({"exercise": serializer.data})

    def put(self, request, group_id, exercise_id):
        answerAuth = authTeacher(request)
        if answerAuth!=None:
            return answerAuth
        else:
            saved_exercise = get_object_or_404(Exercise.objects.all(), id=exercise_id)
            data = request.data.get('exercise')
            serializer = ExerciseSerializer(instance=saved_exercise, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response("задача обновлена", status=200)

    def delete(self, request, group_id, exercise_id):
        answerAuth = authTeacher(request)
        if answerAuth!=None:
            return answerAuth
        else:
            article = get_object_or_404(Exercise.objects.all(), id=exercise_id)
            article.delete()
            return Response("задача удалена", status=200)


class TeacherSolutions(APIView):
    def get(self, request, group_id, exercise_id, format=None):
        answerAuth = authTeacher(request)
        answerGroup = fidelityGroup(group_id)
        answerExercise = fidelityExercise(exercise_id)
        if answerAuth!=None:
            return answerAuth
        elif answerGroup != None:
            return answerGroup
        elif answerExercise != None:
            return answerExercise
        else:
            exercise_id = Exercise.objects.filter(id=exercise_id).filter(group_id=group_id)[0].id
            solutions = Solution.objects.filter(exercise_id=exercise_id)
            serializer = SolutionSerializer(solutions, many=True, context={'request': request})
            return Response({"solution": serializer.data})


class TeacherSolution(APIView):
    def get(self, request, group_id, exercise_id, solution_id, format=None):
        answerAuth = authTeacher(request)
        answerGroup = fidelityGroup(group_id)
        answerExercise = fidelityExercise(exercise_id)
        answerSolution = fidelitySolution(solution_id)
        if answerAuth!=None:
            return answerAuth
        elif answerGroup != None:
            return answerGroup
        elif answerExercise != None:
            return answerExercise
        elif answerSolution != None:
            return answerSolution
        else:
            exercise_id = Exercise.objects.filter(id=exercise_id).filter(group_id=group_id)[0].id
            solutions = Solution.objects.filter(id=solution_id).filter(exercise_id=exercise_id)
            serializer = SolutionSerializer(solutions, many=True, context={'request': request})
            return Response({"solution": serializer.data})

    def put(self, request, group_id, exercise_id, solution_id, format=None):
        answerAuth = authTeacher(request)
        if answerAuth!=None:
            return answerAuth
        else:
            saved_solution = get_object_or_404(Solution.objects.all(), id=solution_id)
            data = request.data.get('solution')
            serializer = SolutionSerializer(instance=saved_solution, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response("ответ обновлен", status=200)


class StudentTrainingClass(APIView):
    def get(self, request, format=None):
        answerAuth = authStudent(request)
        if answerAuth!=None:
            return answerAuth
        else:
            user_id = auth.get_user(request).id
            student = Student.objects.get(user_id=user_id)
            groups = Group.objects.filter(student=student)
            serializer = UserSerializer(groups, many=True)
            return Response(serializer.data)


class StudentExercises(APIView):
    def get(self, request, group_id, format=None):
        answerAuth = authStudent(request)
        answerGroup = fidelityGroup(group_id)
        if answerAuth!=None:
            return answerAuth
        elif answerGroup!=None:
            return answerGroup
        else:
            exercise = Exercise.objects.filter(group_id=group_id)
            serializer = ExerciseSerializer(exercise, many=True)
            return Response({"exercise": serializer.data})


class StudentExercise(APIView):
    def get(self, request, group_id, exercise_id, format=None):
        answerAuth = authStudent(request)
        answerGroup = fidelityGroup(group_id)
        answerExercise = fidelityExercise(exercise_id)
        if answerAuth!=None:
            return answerAuth
        elif answerGroup != None:
            return answerGroup
        elif answerExercise != None:
            return answerExercise
        else:
            exercise = Exercise.objects.filter(group_id=group_id).filter(id=exercise_id)
            serializer = ExerciseSerializer(exercise, many=True, context={'request': request})
            return Response({"exercise": serializer.data})


class StudentSolutions(APIView):
    def get(self, request, group_id, exercise_id, format=None):
        answerAuth = authStudent(request)
        answerGroup = fidelityGroup(group_id)
        answerExercise = fidelityExercise(exercise_id)
        if answerAuth!=None:
            return answerAuth
        elif answerGroup != None:
            return answerGroup
        elif answerExercise != None:
            return answerExercise
        else:
            student = Student.objects.get(user_id=auth.get_user(request).id)
            exercise_id = Exercise.objects.filter(id=exercise_id).filter(group_id=group_id)[0].id
            solutions = Solution.objects.filter(exercise_id=exercise_id).filter(student_id=student)
            serializer = SolutionSerializer(solutions, many=True, context={'request': request})
            return Response({"solution": serializer.data})

    def post(self, request, group_id, exercise_id, format=None):
        answer = authStudent(request)
        if answer!=None:
            return answer
        else:
            if Solution.objects.filter(id=auth.get_user(request).id).count() == 0:
                solution = request.data.get("solution")
                serializer = SolutionSerializer(data=solution)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                return Response("ответ добавлен", status=201)
            else:
                return Response("новый ответ создать нельзя, можно изменит существующий", status=422)


class StudentSolution(APIView):
    def get(self, request, group_id, exercise_id, solution_id, format=None):
        answerAuth = authStudent(request)
        answerGroup = fidelityGroup(group_id)
        answerExercise = fidelityExercise(exercise_id)
        answerSolution = fidelitySolution(solution_id)
        if answerAuth!=None:
            return answerAuth
        elif answerGroup != None:
            return answerGroup
        elif answerExercise != None:
            return answerExercise
        elif answerSolution != None:
            return answerSolution
        else:
            student = Student.objects.get(user_id=auth.get_user(request).id)
            exercise_id = Exercise.objects.filter(id=exercise_id).filter(group_id=group_id)[0].id
            solutions = Solution.objects.filter(exercise_id=exercise_id).filter(student_id=student).filter(id=solution_id)
            serializer = SolutionSerializer(solutions, many=True, context={'request': request})
            return Response({"solution": serializer.data})

    def put(self, request, group_id, exercise_id, solution_id, format=None):
        answer = authStudent(request)
        if answer!=None:
            return answer
        else:
            saved_solution = get_object_or_404(Solution.objects.all(), id=solution_id)
            data = request.data.get('solution')
            serializer = SolutionSerializer(instance=saved_solution, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response("ответ обновлен", status=200)
