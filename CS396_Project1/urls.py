"""
URL configuration for CS396_Project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('', include('DiscussionBoard.urls')),
    path('users/', include('users.urls')),
    path('teacher/report/', user_views.teacher_report, name='teacher_report'),
    path('student/report/', user_views.student_report, name='student_report'),
    path('create-quiz/', user_views.create_quiz, name='create-quiz'),
    path('quiz/<int:quiz_id>/create_question/', user_views.create_questions, name='create_questions'),
    path('question/<int:question_id>/add_choices/', user_views.add_choices, name='add_choices'),
    path('create_quiz/', user_views.create_quiz, name='create_quiz'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)