from rest_framework import serializers
from .models import Service, Appointment
from users.serializers import UserSerializer
from users.models import User

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    vet = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_vet=False),
        source='client',
        write_only=True
    )
    vet_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_vet=True),
        source='vet',
        write_only=True
    )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True
    )

    class Meta:
        model = Appointment
        fields = ('id', 'client', 'vet', 'service', 'client_id', 'vet_id', 'service_id',
                 'date', 'time', 'status', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at') 