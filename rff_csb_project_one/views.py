from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Refill, Recharge, PluginHybridVehicle, MidHybridVehicle, FlexFuelVehicle, FuelVehicle, GasVehicle, ElectricVehicle, Vehicle

def root(request):
    return render(request, 'pages/debugging_page.html')

def landing(request):
    vehicles = list(Vehicle.objects.select_related('electricvehicle','gasvehicle','fuelvehicle','flexfuelvehicle','midhybridvehicle','pluginhybridvehicle').all().values())
    print(vehicles)
    return render(request, 'pages/frontpage.html', {'vehicles': vehicles})

def login(request):
    return None

def logout(request):
    return None

@csrf_exempt
def debug_reset_vehicles(request):
    with transaction.atomic():
        Vehicle.objects.select_related('electricvehicle','gasvehicle','fuelvehicle','flexfuelvehicle','midhybridvehicle','pluginhybridvehicle').all().delete()
        return redirect('debug_whathaveyoudone')

@csrf_exempt
def debug_reset_refills(request):
    with transaction.atomic():
        Refill.objects.all().delete()
        return redirect('debug_whathaveyoudone')

@csrf_exempt
def debug_reset_recharges(request):
    with transaction.atomic():
        Recharge.objects.all().delete()
        return redirect('debug_whathaveyoudone')

@csrf_exempt
def debug_whathaveyoudone(request):
    return render(request, 'pages/debugging_whathaveyoudone.html')

@csrf_exempt
def add_vehicle_phase1(request):
    return render(request, 'pages/addvehicle_phase1.html')

@csrf_exempt
def add_vehicle_phase2(request):
    if request.method == "POST" and request.POST['phase'] == '1':
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        additional_model_details = request.POST['additional_model_info']
        odometer = request.POST['odo']
        rental_or_loan = request.POST['rental_loaner']
        licence_plate = request.POST['licence']
        vehicle_type = request.POST['vehicle_type']
        prefilled = {
            'make': make,
            'model': model,
            'year': int(year),
            'additional_model_info': additional_model_details,
            'odo': int(odometer),
            'rental_loaner': rental_or_loan,
            'licence': licence_plate,
            'vehicle_type': vehicle_type
        }
        return render(request, 'pages/addvehicle_phase2.html', {'prefilled': prefilled})
    return redirect('/')

@csrf_exempt
def submit_vehicle(request):
    if 'phase' in request.POST and request.POST['phase'] == '2':
        make = request.POST['make']
        model = request.POST['model']
        year = int(request.POST['year'])
        additional_model_details = request.POST['additional_model_info']
        odometer = int(request.POST['odo'])
        rental_or_loan = request.POST['rental_loaner']
        licence_plate = request.POST['licence']
        vehicle_type = request.POST['vehicle_type']
        nickname = request.POST['vehicle_nickname']
        winter_tires = int(request.POST['winter_tires'])
        with transaction.atomic():
            if vehicle_type == 'Electric':
                try:
                    battery_capacity_kwh = float(request.POST['battery_capacity'])
                    charge_level = int(request.POST['charge_level'])
                    vehicle = ElectricVehicle.objects.create(
                        make=make,
                        model=model,
                        year=year,
                        additional_model_details=additional_model_details,
                        odometer=odometer,
                        rental_or_loan=bool(rental_or_loan == 'yes'),
                        licence_plate=licence_plate,
                        capacity_kwh=battery_capacity_kwh,
                        charge_level=charge_level,
                        nickname=nickname,
                        running_on_winter_tires=bool(winter_tires > 0)
                    )
                    vehicle.set_vehicle_type('EV')
                    vehicle.save()
                except Exception as e:
                    print(e)
                    return redirect('/')
            elif vehicle_type == 'fuel':
                try:
                    fuel_type = request.POST['fuel_type']
                    if fuel_type == 'G':
                        fuel_capacity_kg = float(request.POST['fuel_capacity'])
                        fuel_level_kg = float(request.POST['fuel_level'])*fuel_capacity_kg
                        vehicle = GasVehicle.objects.create(
                            make=make,
                            model=model,
                            year=year,
                            additional_model_details=additional_model_details,
                            odometer=odometer,
                            rental_or_loan=bool(rental_or_loan == 'yes'),
                            licence_plate=licence_plate,
                            capacity_kg=fuel_capacity_kg,
                            level_kg=fuel_level_kg,
                            nickname=nickname,
                            running_on_winter_tires=bool(winter_tires > 0)
                        )
                        vehicle.set_vehicle_type('CGV')
                        vehicle.save()
                    else:
                        fuel_capacity_l = float(request.POST['fuel_capacity'])
                        fuel_level_l = float(request.POST['fuel_level'])*fuel_capacity_l
                        vehicle = FuelVehicle.objects.create(
                            make=make,
                            model=model,
                            year=year,
                            additional_model_details=additional_model_details,
                            odometer=odometer,
                            rental_or_loan=bool(rental_or_loan == 'yes'),
                            licence_plate=licence_plate,
                            capacity_l=fuel_capacity_l,
                            fuel_level_l=fuel_level_l,
                            nickname=nickname,
                            running_on_winter_tires=bool(winter_tires > 0)
                        )
                        vehicle.set_vehicle_type('SFV')
                        vehicle.set_fuel_type(fuel_type)
                        vehicle.save()
                except Exception as e:
                    print(e)
                    return redirect('/')
            elif vehicle_type == 'BE':
                try:
                    flex_capacity_1 = float(request.POST['fuel_capacity'])
                    flex_level_1 = float(request.POST['fuel_level'])*fuel_capacity_l
                    vehicle = FlexFuelVehicle.objects.create(
                        make=make,
                        model=model,
                        year=year,
                        additional_model_details=additional_model_details,
                        odometer=odometer,
                        rental_or_loan=bool(rental_or_loan == 'yes'),
                        licence_plate=licence_plate,
                        fuel_capacity_l=flex_capacity_1,
                        fuel_level_l=flex_level_1,
                        nickname=nickname,
                        running_on_winter_tires=bool(winter_tires > 0)
                    )
                    vehicle.set_vehicle_type('FFVE')
                    vehicle.set_flex_fuel_type('BE')
                    vehicle.save()
                except Exception as e:
                    print(e)
                    return redirect('/')
            elif vehicle_type == 'BG':
                print(request.POST)
                try:
                    flex_capacity_1 = float(request.POST['fuel_capacity'])
                    flex_level_1 = float(request.POST['fuel_level'])*flex_capacity_1
                    flex_capacity_2 = float(request.POST['fuel_capacity_g'])
                    flex_level_2 = float(request.POST['fuel_level_g'])*flex_capacity_2
                    vehicle = FlexFuelVehicle.objects.create(
                        make=make,
                        model=model,
                        year=year,
                        additional_model_details=additional_model_details,
                        odometer=odometer,
                        rental_or_loan=bool(rental_or_loan == 'yes'),
                        licence_plate=licence_plate,
                        fuel_capacity_l=flex_capacity_1,
                        fuel_level_l=flex_level_1,
                        cng_capacity_kg=flex_capacity_2,
                        cng_level_kg=flex_level_2,
                        nickname=nickname,
                        running_on_winter_tires=bool(winter_tires > 0)
                    )
                    vehicle.set_vehicle_type('FFVG')
                    vehicle.set_flex_fuel_type('BG')
                    vehicle.save()
                except Exception as e:
                    print(e)
                    return redirect('/')
            elif vehicle_type == 'MHEV':
                try:
                    fuel_capacity_l = float(request.POST['fuel_capacity'])
                    fuel_level_l = float(request.POST['fuel_level'])*fuel_capacity_l
                    fuel_type = request.POST['hybrid_fuel']
                    battery_capacity_kwh = float(request.POST['battery_capacity'])
                    vehicle = MidHybridVehicle.objects.create(
                        make=make,
                        model=model,
                        year=year,
                        additional_model_details=additional_model_details,
                        odometer=odometer,
                        rental_or_loan=bool(rental_or_loan == 'yes'),
                        licence_plate=licence_plate,
                        capacity_l=fuel_capacity_l,
                        level_l=fuel_level_l,
                        battery_capacity_kwh=battery_capacity_kwh,
                        nickname=nickname,
                        running_on_winter_tires=bool(winter_tires > 0)
                    )
                    vehicle.set_vehicle_type('MHEV')
                    vehicle.set_fuel_type(fuel_type)
                    vehicle.save()
                except Exception as e:
                    print(e)
                    return redirect('/')
            elif vehicle_type == 'PHEV':
                try:
                    fuel_capacity_l = float(request.POST['fuel_capacity'])
                    fuel_level_l = float(request.POST['fuel_level'])*fuel_capacity_l
                    fuel_type = request.POST['hybrid_fuel']
                    battery_capacity_kwh = float(request.POST['battery_capacity'])
                    charge_level = int(request.POST['charge_level'])
                    vehicle = PluginHybridVehicle.objects.create(
                        make=make,
                        model=model,
                        year=year,
                        additional_model_details=additional_model_details,
                        odometer=odometer,
                        rental_or_loan=bool(rental_or_loan == 'yes'),
                        licence_plate=licence_plate,
                        capacity_l=fuel_capacity_l,
                        level_l=fuel_level_l,
                        battery_capacity_kwh=battery_capacity_kwh,
                        charge_level=charge_level,
                        nickname=nickname,
                        running_on_winter_tires=bool(winter_tires > 0)
                    )
                    vehicle.set_vehicle_type('PHEV')
                    vehicle.set_fuel_type(fuel_type)
                    vehicle.save()
                except Exception as e:
                    print(e)
                    return redirect('/')
    return redirect('/')

def manage_vehicle(request, vehicle_id):
    if request.method == "GET":
        vehicle = Vehicle.objects.get(id=vehicle_id)
        if vehicle.vehicle_type_shorthand == 'EV':
            vehicle = ElectricVehicle.objects.get(id=vehicle_id)
        elif vehicle.vehicle_type_shorthand == 'CGV':
            vehicle = GasVehicle.objects.get(id=vehicle_id)
        elif vehicle.vehicle_type_shorthand == 'SFV':
            vehicle = FuelVehicle.objects.get(id=vehicle_id)
        elif vehicle.vehicle_type_shorthand == 'FFVE' or vehicle.vehicle_type_shorthand == 'FFVG':
            vehicle = FlexFuelVehicle.objects.get(id=vehicle_id)
        elif vehicle.vehicle_type_shorthand == 'MHEV':
            vehicle = MidHybridVehicle.objects.get(id=vehicle_id)
        elif vehicle.vehicle_type_shorthand == 'PHEV':
            vehicle = PluginHybridVehicle.objects.get(id=vehicle_id)
        vehicle_details = {
            'id': vehicle.id,
            'make': vehicle.make,
            'model': vehicle.model,
            'year': vehicle.year,
            'additional_model_details': vehicle.additional_model_details,
            'odometer': vehicle.odometer,
            'rental_or_loan': vehicle.rental_or_loan,
            'licence_plate': vehicle.licence_plate,
            'vehicle_type': vehicle.vehicle_type,
            'vehicle_type_shorthand': vehicle.vehicle_type_shorthand,
            'is_vehicle_on_winter_tires': vehicle.running_on_winter_tires,
            'recommended_tire_pressure_front': vehicle.recommended_tire_pressure_front,
            'recommended_tire_pressure_rear': vehicle.recommended_tire_pressure_rear,
            'front_pressure': vehicle.front_pressure,
            'rear_pressure': vehicle.rear_pressure
        }

        if vehicle.nickname:
            vehicle_details['vehicle_header'] = vehicle.nickname
        else:
            vehicle_details['vehicle_header'] = f"{vehicle.make} {vehicle.model} - {vehicle.licence_plate}"
        if vehicle.vehicle_type_shorthand == 'EV':
            vehicle_details['capacity_kwh'] = vehicle.capacity_kwh
            vehicle_details['charge_level'] = vehicle.charge_level
            recharges = list(Recharge.objects.filter(vehicle=vehicle).values())
            vehicle_details['recharges'] = recharges
        elif vehicle.vehicle_type_shorthand == 'CGV':
            vehicle_details['capacity_kg'] = vehicle.capacity_kg
            vehicle_details['level_kg'] = vehicle.level_kg
            refuelings = list(Refill.objects.filter(vehicle=vehicle).values())
            vehicle_details['refuelings'] = refuelings
        elif vehicle.vehicle_type_shorthand == 'SFV':
            vehicle_details['capacity_l'] = vehicle.capacity_l
            vehicle_details['level_l'] = vehicle.fuel_level_l
            vehicle_details['fuel_type'] = vehicle.fuel_type
            vehicle_details['fuel_type_shorthand'] = vehicle.fuel_type_shorthand
            refuelings = list(Refill.objects.filter(vehicle=vehicle).values())
            vehicle_details['refuelings'] = refuelings
        elif vehicle.vehicle_type_shorthand == 'FFVE':
            vehicle_details['capacity_l'] = vehicle.fuel_capacity_l
            vehicle_details['level_l'] = vehicle.fuel_level_l
            vehicle_details['fuel_type_shorthand'] = vehicle.flex_fuel_type_shorthand
            vehicle_details['fuel_type'] = vehicle.flex_fuel_type
            refuelings = list(Refill.objects.filter(vehicle=vehicle).values())
            vehicle_details['refuelings'] = refuelings
        elif vehicle.vehicle_type_shorthand == 'FFVG':
            vehicle_details['capacity_l'] = vehicle.fuel_capacity_l
            vehicle_details['level_l'] = vehicle.fuel_level_l
            vehicle_details['capacity_kg'] = vehicle.cng_capacity_kg
            vehicle_details['level_kg'] = vehicle.cng_level_kg
            vehicle_details['fuel_type_shorthand'] = vehicle.flex_fuel_type_shorthand
            vehicle_details['fuel_type'] = vehicle.flex_fuel_type
            refuelings = list(Refill.objects.filter(vehicle=vehicle).values())
            vehicle_details['refuelings'] = refuelings
        elif vehicle.vehicle_type_shorthand == 'MHEV':
            vehicle_details['capacity_l'] = vehicle.capacity_l
            vehicle_details['level_l'] = vehicle.level_l
            vehicle_details['fuel_type_shorthand'] = vehicle.fuel_type_shorthand
            vehicle_details['fuel_type'] = vehicle.fuel_type
            vehicle_details['battery_capacity_kwh'] = vehicle.battery_capacity_kwh
            refuelings = list(Refill.objects.filter(vehicle=vehicle).values())
            vehicle_details['refuelings'] = refuelings
        elif vehicle.vehicle_type_shorthand == 'PHEV':
            vehicle_details['capacity_l'] = vehicle.capacity_l
            vehicle_details['level_l'] = vehicle.level_l
            vehicle_details['fuel_type_shorthand'] = vehicle.fuel_type_shorthand
            vehicle_details['fuel_type'] = vehicle.fuel_type
            vehicle_details['battery_capacity_kwh'] = vehicle.battery_capacity_kwh
            vehicle_details['charge_level'] = vehicle.charge_level
            recharges = list(Recharge.objects.filter(vehicle=vehicle).values())
            vehicle_details['recharges'] = recharges
            refuelings = list(Refill.objects.filter(vehicle=vehicle).values())
            vehicle_details['refuelings'] = refuelings
        print(vehicle_details)
        return render(request, 'pages/vehicle.html', {'details': vehicle_details})
    return redirect('/')

@csrf_exempt
def remove_vehicle(request):
    return None

@csrf_exempt
def submit_refill(request):
    if request.method == "POST":
        with transaction.atomic():
            fill_amount = float(request.POST['fill_amount'])
            fuel_level = float(request.POST['fuel_level'])
            location= request.POST['refill_location']
            vehicle = Vehicle.objects.get(id=request.POST['vehicle_id'])
            price = float(request.POST['price'])
            refill_type = request.POST['refill_type']
            odo = int(request.POST['odometer_reading'])
            distance = float(request.POST['distance_covered'])
            notes = request.POST['notes']
            if vehicle.vehicle_type_shorthand == 'CGV' and refill_type in ['CBG','CNG']:
                vehicle = GasVehicle.objects.get(id=request.POST['vehicle_id'])
            elif vehicle.vehicle_type_shorthand == 'FFVG' and refill_type in ['CBG','CNG','B','E']:
                vehicle = FlexFuelVehicle.objects.get(id=request.POST['vehicle_id'])
            elif vehicle.vehicle_type_shorthand == 'SFV' and refill_type in ['B','D','E']:
                vehicle = FuelVehicle.objects.get(id=request.POST['vehicle_id'])
            elif vehicle.vehicle_type_shorthand == 'MHEV' and refill_type in ['B','D']:
                vehicle = MidHybridVehicle.objects.get(id=request.POST['vehicle_id'])
            elif vehicle.vehicle_type_shorthand == 'PHEV' and refill_type in ['B','D']:
                vehicle = PluginHybridVehicle.objects.get(id=request.POST['vehicle_id'])
            next = request.POST.get('next', '/')
            try:
                if vehicle.vehicle_type_shorthand in ['FFVG', 'FFVE']:
                    vehicle.refill(refill_type, fuel_level)
                else:
                    vehicle.refill(fuel_level)
                vehicle.update_odometer(odo)
                vehicle.save()
                refill = Refill.objects.create(
                    vehicle=vehicle,
                    refill_location=location,
                    amount=fill_amount,
                    price=price,
                    refill_type=refill_type,
                    odometer_reading=odo,
                    distance=distance,
                    notes=notes,
                    fuel_level=fuel_level,
                    winter_tires=vehicle.running_on_winter_tires,
                    average_consumption=round(fill_amount/distance, 2)
                )
                refill.save()
            except Exception as e:
                print(e)
            return redirect(next)
    return redirect('/')

@csrf_exempt
def remove_refill(request):
    if request.method == "POST":
        with transaction.atomic():
            next = request.POST.get('next', '/')
            try:
                Refill.objects.get(id=request.POST['refill_id']).delete()
            except Exception as e:
                print(e)
            return redirect(next)
    return redirect('/')

@csrf_exempt
def submit_recharge(request):
    if request.method == "POST":
        with transaction.atomic():
            location = request.POST['recharge_location']
            amount = float(request.POST['recharged_kwh'])
            charge_to = int(request.POST['charge_to'])
            price = float(request.POST['price'])
            distance_covered = float(request.POST['distance_covered'])
            odometer_reading = int(request.POST['odometer_reading'])
            notes = request.POST['notes']
            vehicle = Vehicle.objects.get(id=request.POST['vehicle_id'])
            if vehicle.vehicle_type_shorthand == 'EV':
                vehicle = ElectricVehicle.objects.get(id=request.POST['vehicle_id'])
            elif vehicle.vehicle_type_shorthand == 'PHEV':
                vehicle = PluginHybridVehicle.objects.get(id=request.POST['vehicle_id'])
            next = request.POST.get('next', '/')
            try:
                vehicle.recharge(charge_to)
                vehicle.update_odometer(odometer_reading)
                vehicle.save()
                recharge = Recharge.objects.create(
                    vehicle=vehicle,
                    level_charged_to=charge_to,
                    price=price,
                    odometer_reading=odometer_reading,
                    distance=distance_covered,
                    notes=notes,
                    recharge_location=location,
                    recharged_kwh=amount,
                    winter_tires=vehicle.running_on_winter_tires,
                    average_consumption=round(amount/distance_covered, 2)
                )
                recharge.save()
            except Exception as e:
                print(e)
            return redirect(next)
    return redirect('/')

@csrf_exempt
def remove_recharge(request):
    if request.method == "POST":
        with transaction.atomic():
            next = request.POST.get('next', '/')
            try:
                Recharge.objects.get(id=request.POST['recharge_id']).delete()
            except Exception as e:
                print(e)
            return redirect(next)
    return redirect('/')

