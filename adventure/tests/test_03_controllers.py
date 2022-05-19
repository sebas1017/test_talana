
import pytest
from django.core import mail

from adventure import models, notifiers, repositories, usecases, views
from datetime import date
from .test_02_usecases import MockJourneyRepository

#########
# Tests #
#########


class TestRepository:
    def test_create_vehicle(self, mocker):
        mocker.patch.object(models.Vehicle.objects, "create")
        repo = repositories.JourneyRepository()
        car = models.VehicleType()
        repo.create_vehicle(name="a", passengers=10, vehicle_type=car)
        assert models.Vehicle.objects.create.called


class TestNotifier:
    def test_send_notification(self, mocker):
        mocker.patch.object(mail, "send_mail")
        notifier = notifiers.Notifier()
        notifier.send_notifications(models.Journey())
        assert mail.send_mail.called


class TestCreateVehicleAPIView:
    def test_create(self, client, mocker):
        vehicle_type = models.VehicleType(name="car")
        mocker.patch.object(
            models.VehicleType.objects, "get", return_value=vehicle_type
        )
        mocker.patch.object(
            models.Vehicle.objects,
            "create",
            return_value=models.Vehicle(
                id=1, name="Kitt", passengers=4, vehicle_type=vehicle_type
            ),
        )

        payload = {"name": "Kitt", "passengers": 4, "vehicle_type": "car"}
        response = client.post("/api/adventure/create-vehicle/", payload)
        assert response.status_code == 201


class TestStartJourneyAPIView:
    def test_api(self, client, mocker):
        mocker.patch.object(
            views.StartJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )

        payload = {"name": "Kitt", "passengers": 2}
        response = client.post("/api/adventure/start/", payload)

        assert response.status_code == 201

    def test_api_fail(self, client, mocker):
        mocker.patch.object(
            views.StartJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )
        payload = {"name": "Kitt", "passengers": 6}
        response = client.post("/api/adventure/start/", payload)

        assert response.status_code == 400
@pytest.mark.django_db
class TestStopJourneyAPIView:
    def test_api(self, client, mocker):
        models.VehicleType.objects.get_or_create(name="car", max_capacity=5)
        payload = {"name": "chevrolet", "passengers": 4, "vehicle_type": "car"}
        client.post("/api/adventure/create-vehicle/", payload)
        vehicle = models.Vehicle.objects.all()[0]
        id_vehicle_to_stop = vehicle.id
        models.Journey.objects.create(
            vehicle=vehicle, start=date.today()
        )
    
        for _test in range(1,4):
            if _test == 3:
                payload_stop = {"id":100}
            elif _test <3:    
                payload_stop = {"id":id_vehicle_to_stop}
            response_stop_api= client.post("/api/adventure/stop/", payload_stop)
            if _test == 1:
                assert response_stop_api.status_code == 201
                assert response_stop_api.json() == {'message': 'successfully stopped vehicle'}
            elif _test == 2:
                assert response_stop_api.status_code == 200
                assert response_stop_api.json() == {"message":"The vehicle is not moving"}
            elif _test == 3:
                assert response_stop_api.status_code == 400
                assert response_stop_api.json() ==  {"message":"The vehicle you want to stop does not exist"}




       
        
            
