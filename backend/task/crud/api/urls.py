from django.urls import path

from crud.api.views import CrudService
from django_grpc_framework import views as grpc_views


urlpatterns = [
    path('grpc/CrudService/', grpc_views.gRpcService.as_view(CrudService), name='CrudService'),
]