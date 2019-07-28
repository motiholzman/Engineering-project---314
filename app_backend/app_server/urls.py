from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import generateWords

from app_server import views

urlpatterns = [
    path('app_server/question/', views.QuestionsList.as_view(), name='Questions-list'),
    path('app_server/question/<int:pk>/', views.QuestionsDetail.as_view(), name='Questions-list-by-id'),
    path('users/', views.UserList.as_view(), name='Users-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='Users-list-by-id'),
    path('app_server/AddAnswerToDB/', views.AddAnswerToDB.as_view(), name='Answer-post'),
    re_path('app_server/getQuestionByTopic/.+', views.GetQuestionsByTopic.as_view(), name='Question-getter'),
    re_path('app_server/getReviewByTopic/.+', views.GetReviewByTopic.as_view(), name='Review-getter'),
    re_path('app_server/UpdateAnswerCount/.+', views.UpdateAnswerCount.as_view(), name='Answer-update'),
    path('app_server/upload-csv/', views.question_upload, name='Question-CSV-upload'),
    path('app_server/establish_session/', views.EstablishSession.as_view(), name='Establish-Session'),
    path('app_server/GetScore/', views.GetScore.as_view(), name='Get-score'),
    path('app_server/GetTopScore/', views.GetTopScore.as_view(), name='Get-Top-Score'),
    # this path is used for initialize the db
    path('app_server/init_db/', generateWords.init_database, name='initializing-db'),
    path('', views.api_root)
]

urlpatterns = format_suffix_patterns(urlpatterns)