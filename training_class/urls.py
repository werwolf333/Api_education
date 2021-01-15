from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'training_class'

urlpatterns = [
    path('teacher-api/groups', views.TeacherTrainingClass.as_view(), name='TrainingClassTeacher'),
    path('teacher-api/groups/<str:group_id>/exercises', views.TeacherExercises.as_view(), name='TeacherExercises'),
    path('teacher-api/groups/<str:group_id>/exercises/<int:exercise_id>', views.TeacherExercise.as_view(), name='TeacherExercise'),
    path('teacher-api/groups/<str:group_id>/exercises/<int:exercise_id>/solutions', views.TeacherSolutions.as_view(), name='TeacherTaskDecision'),
    path('teacher-api/groups/<str:group_id>/exercises/<int:exercise_id>/solutions/<int:solution_id>', views.TeacherSolution.as_view(),
         name='TeacherTaskDecision'),

    path('student-api/groups', views.StudentTrainingClass.as_view(), name='TrainingClassStudentApi'),
    path('student-api/groups/<str:group_id>/exercises', views.StudentExercises.as_view(), name='StudentExerciseApi'),
    path('student-api/groups/<str:group_id>/exercises/<int:exercise_id>', views.StudentExercise.as_view(), name='StudentExercise'),
    path('student-api/groups/<str:group_id>/exercises/<int:exercise_id>/solutions', views.StudentSolutions.as_view(), name='StudentTaskDecision'),
    path('student-api/groups/<str:group_id>/exercises/<int:exercise_id>/solutions/<int:solution_id>', views.StudentSolution.as_view(),
         name='StudentTaskDecision'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

