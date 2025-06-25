from django.contrib import admin
from django.urls import path, include
from ygv.views import (
    editar_perfil,
    enviar_cotizacion,
    generar_reporte_cotizaciones,
    perfil_ingeniero,
    register, 
    home,
    LoginView,
    ingeniero_home,
    constructor_home,
    cliente_home,
    solicitar_cotizacion,
    cotizaciones_pendientes,
    revisar_cotizacion,
    rechazar_cotizacion,
    perfil_cliente,
    detalle_cotizacion,
    generar_contrato_pdf,
    Mantenimiento,
    Construccion,
    Proyectos
)
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/register/', register, name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),  
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # URLs para roles
    path('ingeniero/', ingeniero_home, name='ingeniero_home'),
    path('constructor/', constructor_home, name='constructor_home'),
    path('cliente/', cliente_home, name='cliente_home'),
    
    # URLs de cotizaciones
    path('solicitar/', solicitar_cotizacion, name='solicitar'),
    path('cotizaciones/pendientes/', cotizaciones_pendientes, name='cotizaciones_pendientes'),
    path('cotizacion/revisar/<int:cotizacion_id>/', revisar_cotizacion, name='revisar_cotizacion'),
    path('cotizaciones/<int:id>/rechazar/', rechazar_cotizacion, name='rechazar_cotizacion'),
    path('cotizaciones/<int:id>/', detalle_cotizacion, name='detalle_cotizacion'),
    path('cotizaciones/<int:cotizacion_id>/contrato/', generar_contrato_pdf, name='generar_contrato_pdf'),
    path('cotizaciones/cotizaciones/', generar_reporte_cotizaciones, name='generar_reporte_cotizaciones'),
    path('enviar-cotizacion/<int:cotizacion_id>/', enviar_cotizacion, name='enviar_cotizacion'),
    
    # URL de perfil
    path('ingeniero/perfil/', perfil_ingeniero, name='perfil_ingeniero'),
    path('ingeniero/editar_perfil/', editar_perfil, name='editar_perfil'),
    path('cliente/perfil/', perfil_cliente, name='perfil_cliente'), 

    #URL de servicios
    path('servicios/Mantenimiento/', Mantenimiento, name='Mantenimiento'),
    path('servicios/Construccion/', Construccion, name='Construccion'),
    path('servicios/Proyectos/', Proyectos, name='Proyectos') 


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)