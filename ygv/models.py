from django.db import models
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db.models import Sum, F

class PerfilUsuario(models.Model):
    ROLES = [
        ('cliente', 'Cliente'),
        ('ingeniero', 'Ingeniero'),
        ('constructor', 'Constructor'),
        ('administrador', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    avatar = models.ImageField(
        upload_to='avatars/', 
        default='avatars/default.png', 
        blank=True
    )
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    
    def get_avatar_url(self):
        return self.avatar.url if self.avatar else '/static/images/default-avatar.png'

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
    @receiver(post_save, sender=User)
    def crear_perfil(sender, instance, created, **kwargs):
        if created:
            PerfilUsuario.objects.create(user=instance)

class Actividad(models.Model):
    TIPOS = [
        ('cotizacion', 'Cotización'),
        ('proyecto', 'Proyecto'),
        ('inventario', 'Inventario'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-fecha']

class Proyecto(models.Model):
    tipo_proyecto = models.CharField(max_length=45)
    plazo_proyecto = models.CharField(max_length=45, blank=True, null=True)
    insumos_sobrantes = models.CharField(max_length=45, blank=True, null=True)
    cliente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='proyectos')
    supervisor_mantenimiento = models.CharField(max_length=45, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    disponibilidad_horaria = models.CharField(max_length=45, blank=True, null=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_finalizacion_estimada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ('cliente', 'tipo_proyecto')

    def __str__(self):
        return f"{self.tipo_proyecto} - {self.cliente}"


class Contrato(models.Model):
    tipo_contrato = models.CharField(max_length=45)
    ingeniero = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contrato_ingeniero')
    proveedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contrato_proveedor')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contrato_usuario')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)
    partes_involucradas = models.TextField(blank=True, null=True)
    condiciones_pago = models.TextField(blank=True, null=True)
    penalizaciones = models.TextField(blank=True, null=True)
    descripcion_proyecto = models.TextField(blank=True, null=True)
    modificaciones = models.TextField(blank=True, null=True)
    garantias_seguros = models.TextField(blank=True, null=True)
    doc_adjunta = models.TextField(blank=True, null=True)
    estado_contrato = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.tipo_contrato} - {self.proyecto}"


from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from decimal import Decimal

User = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from decimal import Decimal

User = get_user_model()

class Cotizacion(models.Model):
    """
    Model representing a quotation/estimate in the system.
    Contains all client and project information along with financial calculations.
    """
    
    class Estados(models.TextChoices):
        BORRADOR = 'BORRADOR', 'Borrador'
        EN_REVISION = 'EN_REVISION', 'En revisión'
        APROBADA = 'APROBADA', 'Aprobada'
        RECHAZADA = 'RECHAZADA', 'Rechazada'
        COMPLETADA = 'COMPLETADA', 'Completada'

    class TipoPago(models.TextChoices):
        CONTADO = 'CONTADO', 'Contado'
        CREDITO_30 = 'CREDITO_30', 'Crédito 30 días'
        CREDITO_60 = 'CREDITO_60', 'Crédito 60 días'
        CREDITO_90 = 'CREDITO_90', 'Crédito 90 días'

    class Ciudades(models.TextChoices):
        BOGOTA = 'BOGOTA_DC', 'Bogotá D.C.'
        MEDELLIN = 'MEDELLIN', 'Medellín, Antioquia'
        GIRARDOT = 'GIRARDOT', 'Girardot, Tolima'

    # Client and engineer relationships
    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cotizaciones_como_cliente',
        verbose_name='Cliente'
    )
    ingeniero = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cotizaciones_aprobadas',
        verbose_name='Ingeniero asignado'
    )

    # Basic information
    contacto = models.CharField(
        max_length=100,
        verbose_name='Contacto del cliente'
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    # Project details
    ciudad = models.CharField(
        max_length=45,
        choices=Ciudades.choices,
        default=Ciudades.BOGOTA,
        verbose_name='Ciudad del proyecto'
    )
    tipo_pago = models.CharField(
        max_length=45,
        choices=TipoPago.choices,
        default=TipoPago.CONTADO,
        verbose_name='Tipo de pago'
    )

    # Financial fields
    subtotal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
        verbose_name='Subtotal'
    )
    iva = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
        verbose_name='IVA'
    )
    aplica_iva = models.BooleanField(
        default=True,
        verbose_name='Aplica IVA'
    )
    descuento = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
        verbose_name='Descuento'
    )
    total = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
        verbose_name='Total'
    )

    # Status and notes
    estado = models.CharField(
        max_length=45,
        choices=Estados.choices,
        default=Estados.BORRADOR,
        verbose_name='Estado'
    )
    motivo_rechazo = models.TextField(
        blank=True,
        null=True,
        verbose_name='Motivo de rechazo'
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones adicionales'
    )

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-fecha']
        permissions = [
            ('can_approve_quotation', 'Puede aprobar cotizaciones'),
            ('can_reject_quotation', 'Puede rechazar cotizaciones'),
        ]

    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente.get_full_name() or self.cliente.username}"

    def save(self, *args, **kwargs):
        """
        Override save method to ensure totals are calculated automatically.
        First saves to get PK, then updates totals.
        """
        # First save to get PK if new
        super().save(*args, **kwargs)
        
        # Then update totals
        self.actualizar_totales()

    def actualizar_totales(self):
        """
        Calculates and updates subtotal, tax and total based on items.
        Uses database aggregation for accurate calculations.
        """
        # Calculate subtotal (quantity * unit price for all items)
        resultado = self.items.aggregate(
            subtotal=Sum(F('cantidad') * F('valor_unidad')))
        
        self.subtotal = resultado['subtotal'] or Decimal('0.00')
        
        # Calculate tax (19% if applies)
        self.iva = self.subtotal * Decimal('0.19') if self.aplica_iva else Decimal('0.00')
        
        # Calculate final total
        self.total = self.subtotal + self.iva - self.descuento
        
        # Update only the calculated fields to avoid recursion
        Cotizacion.objects.filter(pk=self.pk).update(
            subtotal=self.subtotal,
            iva=self.iva,
            total=self.total
        )


class CotizacionItem(models.Model):
    """
    Model representing individual items in a quotation.
    Each item has description, quantity, unit of measure and unit price.
    """
    
    class UnidadMedida(models.TextChoices):
        M2 = 'M2', 'Metros cuadrados (m²)'
        ML = 'ML', 'Metros lineales (ml)'
        M3 = 'M3', 'Metros cúbicos (m³)'
        UNIDAD = 'UNIDAD', 'Unidad(es)'
        HORA = 'HORA', 'Hora(s) de trabajo'
        DIA = 'DIA', 'Día(s) de trabajo'
        GALON = 'GALON', 'Galón(es)'
        KG = 'KG', 'Kilogramo(s)'
        LITRO = 'LITRO', 'Litro(s)'

    # Relationship to main quotation
    cotizacion = models.ForeignKey(
        Cotizacion,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Cotización'
    )

    # Item description
    descripcion = models.CharField(
        max_length=255,
        verbose_name='Descripción del trabajo'
    )

    # Quantity and unit of measure
    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Cantidad'
    )
    unidad_medida = models.CharField(
        max_length=10,
        choices=UnidadMedida.choices,
        default=UnidadMedida.UNIDAD,
        verbose_name='Unidad de medida'
    )

    # Unit price (managed internally)
    valor_unidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
        verbose_name='Valor por unidad'
    )

    # Additional notes
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas adicionales'
    )

    class Meta:
        verbose_name = 'Ítem de cotización'
        verbose_name_plural = 'Ítems de cotización'
        ordering = ['id']

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad} {self.get_unidad_medida_display()}"

@property
def valor_total(self):
    """Calcula el valor total del ítem, manejando valores nulos"""
    if self.cantidad is not None and self.valor_unidad is not None:
        return self.cantidad * self.valor_unidad
    return Decimal('0.00')



class Insumo(models.Model):
    tipo = models.CharField(max_length=45, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    proveedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class EntradaInventario(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    ingeniero = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='entrada_ingeniero')
    proveedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='entrada_proveedor')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrada de {self.insumo} para {self.proyecto}"


class SalidaInventario(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Salida asociada al contrato {self.contrato}"


class Sesion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()

    def __str__(self):
        return f"Sesión de {self.usuario.username}"
    
class Alerta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=200)
    nivel = models.CharField(max_length=10, choices=[('info', 'Info'), ('urgente', 'Urgente')])
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
