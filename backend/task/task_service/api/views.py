import json

from django.shortcuts import get_object_or_404

import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer
from .tasks import async_produce_kafka_message, async_produce_nat


class TaskView(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        serialized_message = json.dumps({"message": "Hello Nats"})
        
        # async_produce_nat.apply_async(args=['my_subject', serialized_message], queue='queue_for_task1')
        async_produce_nat.apply_async(args=['my_subject', serialized_message], queue='queue_for_task1')
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            topic = 'test'
            message = json.dumps(serializer.validated_data)
            async_produce_kafka_message.apply_async(args=[topic, message], queue='queue_for_task1')
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response({"detail": "Task Deleted Successfully"},status=status.HTTP_200_OK)
