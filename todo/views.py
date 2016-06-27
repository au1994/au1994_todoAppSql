import django_filters

from django.contrib.auth.models import User

from rest_framework.authentication import BasicAuthentication
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from todo.models import Task
from todo.serializers import TaskSerializer
from todo.serializers import UserSerializer
from todo.serializers import UserPostSerializer
from todo.permissions import IsAdminOrNewUser, IsOwnerOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 1000



class TaskFilter(filters.FilterSet):
    max_due_date = django_filters.DateTimeFilter(name="due_date",
                                            lookup_type="lt")

    class Meta:
        model = Task
        fields = ['max_due_date', 'time', 'is_active', 'is_completed']

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.filter(is_active = True)
    serializer_class = TaskSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):
        user = request.user
        response = {}
        status = {}
        data = {}
        queryset = self.get_queryset()
        queryset = queryset.filter(owner=user)
        queryset = TaskFilter(request.GET, queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = TaskSerializer(queryset, many=True)
 
        if serializer.is_valid():
            status['success'] = False
            error = {}
            error['msg'] = 'Invalid Page'
            status['error'] = error
            response['status'] = status
            return Response(response, status=404)

        status['success']=True
        data['tasks']=serializer.data
        response['status'] = status
        response['data'] = data
        return Response(response)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def delete(self, request, pk):
        task = Task.objects.get(id=pk)
        task.is_active = False
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = (IsAdminOrNewUser,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)



class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
