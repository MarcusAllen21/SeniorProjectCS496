from django.urls import path
from . import views
from .views import QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView, ReplyCreateView

urlpatterns = [
    path('', QuestionListView.as_view(), name='DiscussionBoard-Home'),
    path('post/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('post/new/', QuestionCreateView.as_view(), name='question-create'),
    path('post/<int:pk>/update/', QuestionUpdateView.as_view(), name='question-update'),
    path('post/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),
    path('about/', views.about, name='DiscussionBoard-About'),
    path('post/<int:pk>/reply/', ReplyCreateView.as_view(), name='reply-create'),

]