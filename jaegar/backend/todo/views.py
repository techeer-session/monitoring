from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer
from .tasks import generate_random_number
from celery.result import AsyncResult

class TodoViewSet(ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

class GenerateRandomNumberView(APIView):
    def post(self, request):
        task = generate_random_number.delay()
        return Response({"task_id": task.id})

    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.state == "SUCCESS":
            return Response({"status": result.state, "result": result.result})
        return Response({"status": result.state})
