from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Service, Appointment
from .serializers import ServiceSerializer, AppointmentSerializer

# Create your views here.

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_vet:
            return Appointment.objects.filter(vet=user)
        return Appointment.objects.filter(client=user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        if request.user.is_vet and appointment.vet == request.user:
            appointment.status = 'confirmed'
            appointment.save()
            return Response(AppointmentSerializer(appointment).data)
        return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        if request.user in [appointment.client, appointment.vet]:
            appointment.status = 'cancelled'
            appointment.save()
            return Response(AppointmentSerializer(appointment).data)
        return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        if request.user.is_vet and appointment.vet == request.user:
            appointment.status = 'completed'
            appointment.save()
            return Response(AppointmentSerializer(appointment).data)
        return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
