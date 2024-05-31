from django.contrib import admin
from django.urls import include, path

from .views import debug_reset_vehicles, debug_reset_refills, debug_reset_recharges, debug_whathaveyoudone, root, landing, login, logout, add_vehicle_phase1, add_vehicle_phase2, remove_vehicle, submit_vehicle, manage_vehicle, remove_refill, submit_refill, submit_recharge, remove_recharge

urlpatterns = [
    path('root/', root, name='root'),
    path('', landing, name='landing'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('add_vehicle/1/', add_vehicle_phase1, name='add_vehicle_1'),
    path('add_vehicle/2/', add_vehicle_phase2, name='add_vehicle_2'),
    path('submit_vehicle/', submit_vehicle, name='submit_vehicle'),
    path('remove_vehicle/', remove_vehicle, name='remove_vehicle'),
    path('remove_refill/', remove_refill, name='remove_refill'),
    path('submit_refill/', submit_refill, name='submit_refill'),
    path('submit_recharge/', submit_recharge, name='add_recharge'),
    path('remove_recharge/', remove_recharge, name='remove_recharge'),
    path('debug_reset_vehicles/', debug_reset_vehicles, name='debug_reset_vehicles'),
    path('debug_reset_refills/', debug_reset_refills, name='debug_reset_refills'),
    path('debug_reset_recharges/', debug_reset_recharges, name='debug_reset_recharges'),
    path('debug_whathaveyoudone/', debug_whathaveyoudone, name='debug_whathaveyoudone'),
    path('manage_vehicle/<int:vehicle_id>/', manage_vehicle, name='manage_vehicle'),
]
