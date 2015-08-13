__author__ = 'Jay Modi'

from django.conf.urls import patterns, include, url
from views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserDetails)


urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'registration', CreateUser.as_view(), name='create-user'),
                       )