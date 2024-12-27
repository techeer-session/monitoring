from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User2, Todo2
from .serializers import UserSerializer, TodoSerializer
from .tasks import add_with_delay  # Import the Celery task

class UserViewSet(viewsets.ModelViewSet):
    queryset = User2.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def create_todo(self, request, pk=None):
        user = self.get_object()
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo2.objects.all()
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        serializer.save()
        # Call the Celery task asynchronously
        result = add_with_delay.apply_async((1, 2))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
