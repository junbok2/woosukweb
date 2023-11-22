from django.urls import path
from .views import post_detail, post_delete
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("recruitment", views.recruitment, name="recruitment"),
    path("recruitment_detail/<str:boardid>", views.recruitment_detail, name="recruitment_detail"),
    path("job", views.job, name="job"),
    path("job_search", views.job_search, name="job_search"),
    path("job_detail/<str:pageIndex>&<int:boardid>&<str:search_value>&<str:searchJobCd>", views.job_detail, name="job_detail"),
    path("youthpolicy", views.youthpolicy, name="youthpolicy"),
    path("youthpolicy_detail/<int:pageIndex>&<str:boardid>&<str:search_value>", views.youthpolicy_detail, name="youthpolicy_detail"),
    path("youthpolicy_search", views.youthpolicy_search, name="youthpolicy_search"),
    path("education", views.education, name="education"),
    path('join/', views.join, name='join'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/delete/', post_delete, name='post_delete'),
    path("noticeboard", views.noticeboard, name="noticeboard"),
    path('notice/create/', views.create_notice, name='create_notice'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('notice/<int:pk>/delete/', views.notice_delete, name='notice_delete'),
    path('consulting/', views.consulting, name='consulting'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

]