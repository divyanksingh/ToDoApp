from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from todoapp.custom_filter import ModelResourceCustom, duedate_range_filter
from tastypie.authorization import Authorization, DjangoAuthorization
from todoapp.models import Task



class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        authorization = Authorization()


class TaskResource(ModelResource):
    parent = fields.ForeignKey('todoapp.api.TaskResource', attribute = 'parent', null=True, full=True)
    class Meta:
        queryset = Task.objects.exclude(deleted=True)
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'task'
        authorization = Authorization()
        filtering = {
            'due_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'title': ALL
        }
        ordering = ['due_date']


class FilteredResource(ModelResourceCustom):
    class Meta:
        queryset = Task.objects.exclude(deleted=True)
        allowed_methods = ['get']
        resource_name = 'filter'
        filtering = {
            "during":ALL,
        }
        custom_filters = duedate_range_filter
        ordering = ['due_date']


class SubTaskResource(ModelResource):
    subtasks = fields.ToManyField('todoapp.api.TaskResource', attribute=lambda bundle: Task.objects.filter(parent=bundle.obj, deleted=False), null=True, blank=True, full=True)
    class Meta:
        queryset = Task.objects.exclude(deleted=True)
        allowed_methods = ['get']
        resource_name = 'subtasks'
        filtering = {
            "subtasks": ALL_WITH_RELATIONS
        }
        ordering = ['due_date']



class DeletedTaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.exclude(deleted=False)
        allowed_methods = ['get', 'delete']
        resource_name = 'deleted'
        authorization = Authorization()
        filtering = {
            "deletion_date":['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        ordering = ['due_date']