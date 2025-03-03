from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('registrar-venta/', views.registrar_venta, name='registrar_venta'),
    path('boleta/', views.generar_boleta, name='generar_boleta'),
    path('inventario/', views.inventario, name='inventario'),
    path('inventario-editar/<int:id>/', views.inventario_editar, name='inventario_editar'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]