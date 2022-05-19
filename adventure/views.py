from urllib import response
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from adventure import models, notifiers, repositories, serializers, usecases
from datetime import date


class CreateVehicleAPIView(APIView):
    def post(self, request: Request) -> Response:
        payload = request.data
        try:
            vehicle_type = models.VehicleType.objects.get(name=payload["vehicle_type"])
        except models.VehicleType.DoesNotExist:
            return   Response(
            {
                "message":"The vehicle type doesn't exist , first load de endpoint /start"
            },
            status=201,
        )
        vehicle = models.Vehicle.objects.create(
            name=payload["name"],
            passengers=payload["passengers"],
            vehicle_type=vehicle_type,
        )
        return Response(
            {
                "id": vehicle.id,
                "name": vehicle.name,
                "passengers": vehicle.passengers,
                "vehicle_type": vehicle.vehicle_type.name,
            },
            status=201,
        )


class StartJourneyAPIView(generics.CreateAPIView):
    serializer_class = serializers.JourneySerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.StartJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


#stop journey api view

class StopJourneyAPIView(APIView):
    def post(self, request: Request) -> Response:
        payload = request.data
        try:
            vehicle_type = models.Journey.objects.get(vehicle_id=payload["id"])
            if vehicle_type.end is None:
                vehicle_type.end = date.today()
                vehicle_type.save()
                return Response( {"message":"successfully stopped vehicle"},status=201)    
            else:
                return Response( {"message":"The vehicle is not moving"},status=200)
        except models.Journey.DoesNotExist:
            return Response( {"message":"The vehicle you want to stop does not exist"},status=400)
        

# implementacion adicional opcional
# la vista de creacion de vehiculo no posee un schema personalizado
# para ingresar los parametros del POST atraves de swagger por lo que
# la siguiente implementacion extiende el schema de swagger que esta por defecto
# y permite desde la interfaz de swagger ingresar los parametros que viajan hacia 
# CreateVehicleAPIView en el POST tambien implementa un serializador
# el cual esta comentado en el archivo serializers.py
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter
from adventure.serializers import CreateVehicleSerializer


class CreateVehicleAPIView(APIView):
    serializer_class = serializers.JourneySerializer
    @extend_schema(request=None)
    @extend_schema(parameters=[
        OpenApiParameter(name='name', description='', required=True, type=str),
        OpenApiParameter(name='passengers', description='positive integer field is required', required=True, type=int),
        OpenApiParameter(name='vehicle_type', description='', required=True, type=str)
    ])
    def post(self, request: Request) -> Response:
        payload = request.query_params
        if len (list(payload.keys())) == 0:
            payload = request.data
        try:
            vehicle_type = models.VehicleType.objects.get(name=payload["vehicle_type"])
        except models.VehicleType.DoesNotExist:
            return Response({
                "message","Tipo de vehiculo no registrado intentar nuevamente"},status=404)
        vehicle = models.Vehicle.objects.create(
            name=payload["name"],
            passengers=payload["passengers"],
            vehicle_type=vehicle_type,
        )
        serializer = CreateVehicleSerializer(vehicle)
        return Response(
           serializer.data,
            status=201,
        )

"""