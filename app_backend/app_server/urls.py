from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from app_server import views

urlpatterns = [
    path('app_server/question/', views.QuestionsList.as_view(), name='Questions-list'),
    path('app_server/question/<int:pk>/', views.QuestionsDetail.as_view(), name='Questions-list-by-id'),
    path('users/', views.UserList.as_view(), name='Users-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='Users-list-by-id'),
    path('app_server/AddAnswerToDB/', views.AddAnswerToDB.as_view(), name='Answer-post'),
    re_path('app_server/getQuestionByTopic/.+', views.GetQuestionsByTopic.as_view(), name='Question-getter'),

    path('', views.api_root)
]

urlpatterns = format_suffix_patterns(urlpatterns)