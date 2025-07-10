from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from ygv.views import (
    editar_perfil,
    enviar_cotizacion,
    generar_reporte_cotizaciones,
    guardar_firma,
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
from ygv.forms import CustomPasswordResetForm

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # Authentication
    path('accounts/register/', register, name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),  
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Password Reset
    path('recuperar/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/recuperar/enviado/'
    ), name='password_reset'),
    path('recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/recuperar/completado/'
    ), name='password_reset_confirm'),
    path('recuperar/completado/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Roles
    path('ingeniero/', login_required(ingeniero_home), name='ingeniero_home'),
    path('constructor/', login_required(constructor_home), name='constructor_home'),
    path('cliente/', login_required(cliente_home), name='cliente_home'),
    
    # Cotizaciones (ordenadas de más específicas a menos)
    path('cotizacion/revisar/<int:cotizacion_id>/', login_required(revisar_cotizacion), name='revisar_cotizacion'),
    path('cotizaciones/<int:id>/contrato/', login_required(generar_contrato_pdf), name='generar_contrato_pdf'),
    path('cotizaciones/<int:id>/rechazar/', login_required(rechazar_cotizacion), name='rechazar_cotizacion'),
    path('cotizaciones/<int:id>/', login_required(detalle_cotizacion), name='detalle_cotizacion'),
    path('cotizaciones/reporte/', login_required(generar_reporte_cotizaciones), name='generar_reporte_cotizaciones'),
    path('cotizaciones/pendientes/', login_required(cotizaciones_pendientes), name='cotizaciones_pendientes'),
    path('enviar-cotizacion/<int:cotizacion_id>/', login_required(enviar_cotizacion), name='enviar_cotizacion'),
    path('firmar/<int:cotizacion_id>/', login_required(guardar_firma), name='guardar_firma'),
    path('solicitar/', login_required(solicitar_cotizacion), name='solicitar'),
    
    # Perfiles
    path('ingeniero/perfil/', login_required(perfil_ingeniero), name='perfil_ingeniero'),
    path('ingeniero/editar_perfil/', login_required(editar_perfil), name='editar_perfil'),
    path('cliente/perfil/', login_required(perfil_cliente), name='perfil_cliente'), 

    # Servicios
    path('servicios/Mantenimiento/', Mantenimiento, name='Mantenimiento'),
    path('servicios/Construccion/', Construccion, name='Construccion'),
    path('servicios/Proyectos/', Proyectos, name='Proyectos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)