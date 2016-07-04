from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from push_notifications.models import GCMDevice

from todo.models import Task, Notification

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
		model = Task
		fields = ('id', 'description', 'due_date', 'time', 'is_completed',
                  'is_active', 'is_notified', 'owner', 'last_updated')


class UserSerializer(serializers.ModelSerializer):
    #tasks = serializers.PrimaryKeyRelatedField(many=True,
            #queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active')


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
        fields = ('id', 'username', 'password', 'first_name', 'last_name',
        'is_active')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    print user.id
                    print user.username
                    msg = _('User account is not verified.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs

class GCMDeviceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = GCMDevice
        fields = ('id', 'user', 'active', 'registration_id', 'name')


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('is_active', 'id', 'registration_id', 'title', 'body')


class GooglePlusSerializer(serializers.Serializer):
    email_id = serializers.CharField()
    access_token = serializers.CharField()
    #given_name = serializers.CharField(blank=True)

