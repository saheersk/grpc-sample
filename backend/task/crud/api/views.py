from django_grpc_framework.services import Service

from google.protobuf.timestamp_pb2 import Timestamp

from  crud.api.models import Todo 
from crud.api.crud import Item, ItemID, DeleteResponse, ItemList, Empty


class CrudService(Service):
    def CreateItem(self, request, context):
        # Implement logic to create a Todo item in Django models
        todo = Todo.objects.create(title=request.title, description=request.description)
        return Todo(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            created_at=self._get_timestamp(todo.created_at),
        )

    def GetItem(self, request, context):
        # Implement logic to retrieve a Todo item from Django models
        todo = Todo.objects.get(id=request.id)
        return Todo(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            created_at=self._get_timestamp(todo.created_at),
        )

    def UpdateItem(self, request, context):
        # Implement logic to update a Todo item in Django models
        todo = Todo.objects.get(id=request.id)
        todo.title = request.title
        todo.description = request.description
        todo.save()
        return Todo(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            created_at=self._get_timestamp(todo.created_at),
        )

    def DeleteItem(self, request, context):
        # Implement logic to delete a Todo item from Django models
        try:
            todo = Todo.objects.get(id=request.id)
            todo.delete()
            return DeleteResponse(detail="Item deleted successfully.")
        except Todo.DoesNotExist:
            return DeleteResponse(detail="Item not found.")

    # def ListItems(self, request, context):
    #     # Implement logic to list Todo items from Django models
    #     todos = Todo.objects.all()
    #     todo_list = Todo(items=[self._serialize_todo(todo) for todo in todos])
    #     return todo_list

    def _serialize_todo(self, todo):
        return Todo(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            created_at=self._get_timestamp(todo.created_at),
        )

    def _get_timestamp(self, datetime_obj):
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime_obj)
        return timestamp