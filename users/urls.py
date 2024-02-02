from django.urls import path
from .views import QuizDetailView, submit_quiz
from . import views

urlpatterns = [
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('<int:pk>/submit/', submit_quiz, name='submit_quiz'),
    path('quizzes/', views.quiz_list, name='quiz-list'),
    path('quizzes/<int:pk>/', views.quiz_detail, name='quiz-detail'),
    path('create_quiz/', views.create_quiz, name='create-quiz'),
    path('teacher/report/', views.teacher_report, name='teacher-report'),
    path('quiz-list/', views.quiz_list, name='quiz-list'),
    path('student/report/', views.student_report, name='student-report'),
    path('create-quiz/', views.create_quiz, name='create-quiz'),
    path('quiz/<int:quiz_id>/create_question/', views.create_questions, name='create_questions'),
    path('question/<int:question_id>/add_choices/', views.add_choices, name='add_choices'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
]
