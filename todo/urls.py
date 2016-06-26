from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from todo import views

urlpatterns = [
    url(r'^tasks/$', views.TaskList.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)$', views.TaskDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]
