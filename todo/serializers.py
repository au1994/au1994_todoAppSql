from django.contrib.auth.models import User

from rest_framework import serializers

from todo.models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
		model = Task
		fields = ('id', 'description', 'due_date', 'time', 'is_completed',
                  'is_active', 'owner')


class UserSerializer(serializers.ModelSerializer):
    #tasks = serializers.PrimaryKeyRelatedField(many=True,
            #queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class UserPostSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance 

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
