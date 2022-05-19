from django.db import models

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers


    def get_distribution(self) -> list:
        n = self.passengers
        data = []
        impar = False
        if n%2 !=0:
            impar = True
            n = n+1

        for k in range(1,int((n/2)+1)):
            valores = [True,True]
            if k == int(n/2):
                if impar:
                    valores= [True,False]
                    data.append(valores)
                    break
                data.append(valores)
            data.append(valores)
        return data


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"
    
    def is_finished(self) -> bool:
        if self.end != None:
            return True
        else:
            return False




def validate_number_plate(plate) -> bool:
        count_guions = plate.count("-")
        if count_guions != 2:
            return False
        else:
            plate= plate.split("-")
            if len(plate) > 6:
                return False
            first_segment = list(plate[0])
            first_segment =  [ 1   for letter in first_segment  if letter.isdigit()]
            if len(first_segment) > 0:
                return False
            else:
                segments_finals = list(plate[1]) + list(plate[2])
                segments_finals =  [ 1  for digit in segments_finals if digit.isdigit()]
                if len(segments_finals) != 4:
                    return False
                else:
                    return True