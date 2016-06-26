from django.contrib.auth.models import User

from rest_framework import serializers

from todo.models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
		model = Task
		fields = ('id', 'description', 'due_date', 'time', 'is_completed',
                  'owner')


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True,
            queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'tasks')

