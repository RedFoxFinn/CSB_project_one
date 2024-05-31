from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _

class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        EV = 'EV',_('Electric Vehicle')
        CGV = 'CGV',_('Compressed Gas Vehicle')
        SFV = 'SFV',_('Single Fuel Vehicle')
        FFVE = 'FFVE',_('Flex Fuel Vehicle - Ethanol')
        FFVG = 'FFVG',_('Flex Fuel Vehicle - Gas')
        MHEV = 'MHEV',_('Mid Hybrid Vehicle')
        PHEV = 'PHEV',_('Plugin Hybrid Vehicle')

    make = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    year = models.IntegerField(default=2000)
    additional_model_details = models.CharField(max_length=80)
    odometer = models.IntegerField(default=0)
    rental_or_loan = models.BooleanField(default=False)
    licence_plate = models.CharField(max_length=40)
    nickname = models.CharField(
        max_length=40,
        null=True
    )
    vehicle_type_shorthand = models.CharField(default=VehicleType.EV, choices=VehicleType.choices, max_length=4)
    vehicle_type = models.CharField(default=VehicleType.EV.label, choices=VehicleType.choices, max_length=40)
    running_on_winter_tires = models.BooleanField(default=False)
    recommended_tire_pressure_front = models.FloatField(default=2.5)
    recommended_tire_pressure_rear = models.FloatField(default=2.5)
    front_pressure = models.FloatField(default=2.5)
    rear_pressure = models.FloatField(default=2.5)

    def rename(self, new_name):
        self.nickname = new_name

    def acquire(self):
        self.rental_or_loan = False

    def update_odometer(self, new_reading):
        self.odometer = new_reading

    def update_licence_plate(self, new_plate):
        self.licence_plate = new_plate

    def update_additional_model_details(self, new_details):
        self.additional_model_details = new_details

    def set_vehicle_type(self, vehicle_type):
        self.vehicle_type_shorthand = self.VehicleType[vehicle_type]
        self.vehicle_type = self.VehicleType[vehicle_type].label

    def change_to_winter_tires(self):
        self.running_on_winter_tires = True

    def change_to_summer_tires(self):
        self.running_on_winter_tires = False

    def set_tire_pressure(self, front_pressure, rear_pressure):
        self.front_pressure = front_pressure
        self.rear_pressure = rear_pressure

class ElectricVehicle(Vehicle):
    capacity_kwh = models.FloatField(
        default=45,
        validators=[MinValueValidator(1)]
    ) # kWh capacity
    charge_level = models.IntegerField(
        default=50,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    ) # battery charge percentage

    def recharge(self, charge_to):
        self.charge_level = charge_to

class GasVehicle(Vehicle):
    capacity_kg = models.FloatField(default=5,validators=[MinValueValidator(1)])
    level_kg = models.FloatField(default=2.5,validators=[MinValueValidator(0)])

    def replace_gas_containers(self, new_capacity):
        self.capacity_kg = new_capacity

    def refill(self, fuel_level):
        self.level_kg = round(fuel_level * self.capacity_kg, 1)

class FuelVehicle(Vehicle):
    class FuelType(models.TextChoices):
        D = 'D',_('Diesel')
        E = 'E',_('Ethanol')
        B = 'B',_('Gasoline')

    fuel_type_shorthand = models.CharField(default=FuelType.B, choices=FuelType.choices, max_length=1)
    fuel_type = models.CharField(default=FuelType.B.label, choices=FuelType.choices, max_length=10)
    capacity_l = models.FloatField(
        default=45,
        validators=[MinValueValidator(1)]
    )
    fuel_level_l = models.FloatField(
        default=22.5,
        validators=[MinValueValidator(0)]
    )

    def refill(self, fuel_level):
        self.fuel_level_l = round(fuel_level * self.capacity_l, 1)

    def set_fuel_type(self, fuel_type):
        self.fuel_type_shorthand = self.FuelType[fuel_type]
        self.fuel_type = self.FuelType[fuel_type].label

class FlexFuelVehicle(Vehicle):
    class FlexFuelType(models.TextChoices):
        BE = 'BE',_('Gasoline-Ethanol')
        BG = 'BG',_('Gasoline-CNG')

    flex_fuel_type_shorthand = models.CharField(default=FlexFuelType.BE, choices=FlexFuelType.choices, max_length=2)
    flex_fuel_type = models.CharField(default=FlexFuelType.BE.label, choices=FlexFuelType.choices, max_length=20)
    fuel_capacity_l = models.FloatField(
        default=45,
        validators=[MinValueValidator(1)]
    )
    fuel_level_l = models.FloatField(
        default=22.5,
        validators=[MinValueValidator(0)]
    )
    cng_capacity_kg = models.FloatField(
        default=-1,
        validators=[MinValueValidator(1)]
    )
    cng_level_kg = models.FloatField(
        default=-1,
        validators=[MinValueValidator(0)]
    )

    def replace_gas_containers(self, new_capacity):
        self.cng_capacity_kg = new_capacity
    def refill(self, refill_type, fuel_level):
        if refill_type == self.flex_fuel_type[0] or self.flex_fuel_type == self.FlexFuelType.BE and refill_type == 'E':
            self.fuel_level_l = round(fuel_level * self.fuel_capacity_l, 1)
        elif self.flex_fuel_type == self.FlexFuelType.BG and refill_type in ['CNG','CBG']:
            self.cng_level_kg = round(fuel_level * self.cng_capacity_kg, 1)

    def set_flex_fuel_type(self, fuel_type):
        self.fuel_type_shorthand = self.FlexFuelType[fuel_type]
        self.fuel_type = self.FlexFuelType[fuel_type].label

class MidHybridVehicle(Vehicle):
    class FuelType(models.TextChoices):
        D = 'D',_('Diesel')
        B = 'B',_('Gasoline')

    fuel_type_shorthand = models.CharField(default=FuelType.B, choices=FuelType.choices, max_length=1)
    fuel_type = models.CharField(default=FuelType.B.label, choices=FuelType.choices, max_length=10)

    capacity_l = models.FloatField(
        default=45,
        validators=[MinValueValidator(1)]
    )
    level_l = models.FloatField(
        default=22.5,
        validators=[MinValueValidator(0)]
    )
    battery_capacity_kwh = models.FloatField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def refill(self, fuel_level):
        self.level_l = round(fuel_level * self.capacity_l, 1)

    def set_fuel_type(self, fuel_type):
        self.fuel_type_shorthand = self.FuelType[fuel_type]
        self.fuel_type = self.FuelType[fuel_type].label
    
class PluginHybridVehicle(Vehicle):
    class FuelType(models.TextChoices):
        D = 'D',_('Diesel')
        B = 'B',_('Gasoline')

    fuel_type_shorthand = models.CharField(default=FuelType.B, choices=FuelType.choices, max_length=1)
    fuel_type = models.CharField(default=FuelType.B.label, choices=FuelType.choices, max_length=10)

    capacity_l = models.FloatField(
        default=45,
        validators=[MinValueValidator(1)]
    )
    level_l = models.FloatField(
        default=22.5,
        validators=[MinValueValidator(0)]
    )
    battery_capacity_kwh = models.FloatField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    charge_level = models.IntegerField(
        default=50,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    def refill(self, fuel_level):
        self.level_l = round(fuel_level * self.capacity_l, 1)

    def recharge(self, charge_to):
        self.charge_level = charge_to

    def set_fuel_type(self, fuel_type):
        self.fuel_type_shorthand = self.FuelType[fuel_type]
        self.fuel_type = self.FuelType[fuel_type].label

class Refill(models.Model):
    class RefillType(models.TextChoices):
        D = 'D',_('Diesel')
        E = 'E',_('Ethanol')
        B = 'B',_('Gasoline')
        CNG = 'CNG',_('Compressed Natural Gas')
        CBG = 'CBG',_('Compressed Bio Gas')
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    refill_location = models.CharField(max_length=120, default='')
    amount = models.FloatField(default=1,validators=[MinValueValidator(1)])
    fuel_level = models.FloatField(default=0.5,validators=[MaxValueValidator(1), MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=1,validators=[MinValueValidator(0)])
    refill_type = models.CharField(default=RefillType.B, choices=RefillType.choices, max_length=3)
    odometer_reading = models.IntegerField(default=0)
    distance = models.FloatField(default=0, validators=[MinValueValidator(0)])
    average_consumption = models.FloatField(default=5, validators=[MinValueValidator(0)])
    notes = models.CharField(max_length=160, default='')
    winter_tires = models.BooleanField(default=False)

class Recharge(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    recharge_location = models.CharField(max_length=120, default='Home')
    recharged_kwh = models.FloatField(default=1,validators=[MinValueValidator(0.1)])
    level_charged_to = models.IntegerField(default=50,validators=[MaxValueValidator(100), MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=1,validators=[MinValueValidator(0)])
    odometer_reading = models.IntegerField(default=0)
    distance = models.FloatField(default=0, validators=[MinValueValidator(0)])
    average_consumption = models.FloatField(default=5, validators=[MinValueValidator(0)])
    notes = models.CharField(max_length=160, default='')
    winter_tires = models.BooleanField(default=False)
