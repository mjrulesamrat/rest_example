from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
    # Examples:
    # url(r'^$', 'rest_example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # API endpoints
	url(r'^api/', include(router.urls), name="all_routers"),
    url(r'^api/', include('users.urls'), name="users_routers"),
]
