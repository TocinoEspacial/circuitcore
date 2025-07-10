from django.contrib import admin
from django.urls import path, include
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
    Proyectos,
    generar_factura
)
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from ygv.forms import CustomPasswordResetForm


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
    path('ingeniero/factura', generar_factura, name='generar_factura'),

    #URL de servicios
    path('servicios/Mantenimiento/', Mantenimiento, name='Mantenimiento'),
    path('servicios/Construccion/', Construccion, name='Construccion'),
    path('servicios/Proyectos/', Proyectos, name='Proyectos'),
    path('recuperar/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        html_email_template_name='registration/password_reset_email.html',  # <- ESTA LÍNEA
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/recuperar/enviado/'
    ), name='password_reset'),

    # Confirmación de que el correo fue enviado
    path('recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    # Vista para ingresar la nueva contraseña
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/recuperar/completado/'
    ), name='password_reset_confirm'),

    # Confirmación de contraseña restablecida
    path('recuperar/completado/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('firmar/<int:cotizacion_id>/', guardar_firma, name='guardar_firma'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)