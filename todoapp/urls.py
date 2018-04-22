from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from tastypie.api import Api
from todoapp.api import TaskResource, UserResource, FilteredResource, SubTaskResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(TaskResource())
v1_api.register(FilteredResource())
v1_api.register(SubTaskResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    url('index', views.index, name='index'),
]

urlpatterns += staticfiles_urlpatterns()