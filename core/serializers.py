
from rest_framework import serializers
from .models import User, Attendance, Department, Subject
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'role',
            'full_name', 'roll_number', 'phone',
            'department', 'section', 'year'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

User = get_user_model()

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.CharField()

    def validate(self, data):
        email = (data.get('email') or '').strip()
        if not email:
            raise serializers.ValidationError({"detail": "Email is required."})
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User not found. Use the same email you used when creating the account."})

        # Superusers can always sign in as admin; others must match stored role
        if data['role'] == 'admin' and user.is_superuser:
            pass  # allow
        elif user.role != data['role']:
            raise serializers.ValidationError({"detail": "Incorrect role selected. Choose Admin to sign in as administrator."})

        if not user.check_password(data['password']):
            raise serializers.ValidationError({"detail": "Invalid password."})

        data['user'] = user
        return data



class UserSerializer(serializers.ModelSerializer):
    """Read and update user (e.g. student details). No password exposure."""
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'role',
            'full_name', 'roll_number', 'phone',
            'department', 'section', 'year'
        )
        read_only_fields = ('id', 'username', 'email', 'role')
        extra_kwargs = {}

    def update(self, instance, validated_data):
        # Don't allow changing username/email/role via this serializer
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'code')


class SubjectSerializer(serializers.ModelSerializer):
    department_code = serializers.CharField(source='department.code', read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'code', 'department', 'department_code', 'year', 'semester')
