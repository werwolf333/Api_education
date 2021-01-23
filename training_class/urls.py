from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'training_class'

urlpatterns = [
    path('groups', views.TrainingClass.as_view(), name='TrainingClassTeacher'),
    path('groups/<str:group_id>/exercises', views.Exercises.as_view(), name='Exercises'),
    path('groups/<str:group_id>/exercises/<int:exercise_id>', views.OneExercise.as_view(), name='Exercise'),
    path('groups/<str:group_id>/exercises/<int:exercise_id>/solutions', views.Solutions.as_view(), name='TaskDecision'),
    path('groups/<str:group_id>/exercises/<int:exercise_id>/solutions/<int:solution_id>', views.OneSolution.as_view(),
         name='TaskDecision'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

