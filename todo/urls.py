from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as token_view

from todo import views

urlpatterns = [
    url(r'^tasks/$', views.TaskList.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)$', views.TaskDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-token-auth/', token_view.obtain_auth_token),
    url(r'^tokens/$', views.TokenDetail.as_view()),
    url(r'^gcmdevice/$', views.GCMDeviceList.as_view()),
    url(r'^gcmdevice/(?P<pk>[0-9]+)/$', views.GCMDeviceDetail.as_view()),
    url(r'^notifications/$', views.NotificationList.as_view()),
    url(r'^notifications/(?P<pk>[0-9]+)/$', views.NotificationDetail.as_view()),
    url(r'^googleplus/$', views.GooglePlus.as_view()),

]
