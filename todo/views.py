import django_filters

import collections

from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from push_notifications.models import GCMDevice

from todo.models import Task, Notification
from todo.serializers import TaskSerializer, GooglePlusSerializer
from todo.serializers import UserSerializer
from todo.serializers import UserPostSerializer
from todo.serializers import TokenSerializer
from todo.serializers import GCMDeviceSerializer
from todo.serializers import NotificationSerializer
from todo.permissions import IsAdminOrNewUser, IsOwnerOrReadOnly


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def send_email(user):
    
    u = User.objects.get(username=user)
    
    token = Token.objects.create(user=u)
    token.save()
    rand = u.password[-30:]
    subject = "Todo App Email Verification"
    message = "http://localhost:8000/verify_account.html?id=" + str(u.id) + "&user=" + u.username + "&token=" + str(rand)
    from_email = "abhishek.upadhyay.cse12@iitbhu.ac.in"
    to_email = u.username
    send_mail(subject, message, from_email, [to_email], fail_silently=False)


def get_response(response_data, data_resource):

    response = {}
    status = {}
    data = {}
    status['success'] = True
    data[data_resource] = response_data
    response['status'] = status
    response['data'] = data
    return response


class StandardResultsSetPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 1000



class TaskFilter(filters.FilterSet):

    max_due_date = django_filters.DateTimeFilter(name="due_date",
                                            lookup_type="lt")
    min_due_date = django_filters.DateTimeFilter(name="due_date",
                                            lookup_type="gt")

    class Meta:
        model = Task
        fields = ['max_due_date', 'min_due_date', 'time', 'is_active', 'is_completed']

class TaskList(generics.ListCreateAPIView):

    queryset = Task.objects.filter(is_active = True)
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = TaskFilter
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):

        user = request.user
        queryset = self.get_queryset()
        queryset = queryset.filter(owner=user)
        #queryset = TaskFilter(request.GET, queryset)
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = TaskSerializer(queryset, many=True)
        response = get_response(serializer.data, 'tasks')
        return Response(response)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Task.objects.filter(is_active=True)
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request, pk):
        instance  = self.get_object()
        serializer = self.get_serializer(instance)
        response = get_response(serializer.data, 'task')
        return Response(response)
    
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
        response = get_response(serializer.data, 'users')
        return Response(response)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        username = serializer.initial_data['username']
    
        try: 
            user = User.objects.get(username=username)
            
            pwd = user.password
            
            if pwd == '':
                
                password = serializer.initial_data['password']
                if password is not None:
                    user.set_password(password)
                else:
                    return Response({'error':'password null'}, status=400)

                user.save()
                return Response(serializer.initial_data, status=201)
            else:
                return Response({'error':'user already exists'}, status=400)
        except:
            
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['username']
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            u = User.objects.get(username=user)
            token = Token.objects.create(user=u)
            token.save()
            try:
                send_email(user)
            except:
                print "email sending failed"

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 

    def perform_create(self, serializer):
        serializer.save()
    
 


class UserDetail(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class TokenDetail(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        usr = serializer.initial_data['username']
        try:
            usr = User.objects.get(username=usr)
            
            if usr.password =='':
                return Response({'error':'null password'})

        except:
            print 'in except'

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        u = User.objects.get(username=user)
        
        if u.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'email not verified'})

    def get(self, request):
        user_id = self.request.query_params.get('id', None)
        user = self.request.query_params.get('user', None)
        token = self.request.query_params.get('token', None)
        
        if user_id and user and token:
            u = User.objects.get(username=user)
            pwd = u.password[-30:]
            
            if token == pwd:
                
                u.is_active = True
                u.save()
                
                return Response("user verified")
            else:
                return Response("user not verified")

        else:
            return Response("some fields are missing verified")

class GCMDeviceList(generics.ListCreateAPIView):

    queryset = GCMDevice.objects.all()
    serializer_class = GCMDeviceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GCMDeviceDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = GCMDevice.objects.all()
    serializer_class = GCMDeviceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class NotificationList(generics.ListCreateAPIView):

    queryset = Notification.objects.filter(is_active=True)
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Notification.objects.filter(is_active=True)
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class GooglePlus(APIView):

    def post(self, request):
        serializer = GooglePlusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email_id']
        access_token = serializer.data['access_token']
        #first_name = serializer.data['given_name']
        try:
            user = User.objects.get(username=email)
        except:
            if email and access_token:
                user = User(username=email, is_active=True)
                user.save()
                token = Token.objects.create(user=user)
                token.save()
                return Response({'token': token.key})
            
            else:
                return Response({'error': "some fields are missing"})

        
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
