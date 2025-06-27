from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cotizacion, CotizacionItem

from django import forms
from .models import Cotizacion, CotizacionItem
from django.core.validators import MinValueValidator
from decimal import Decimal

from django import forms
from django.core.validators import MinValueValidator
from .models import Cotizacion, CotizacionItem

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['aplica_iva', 'descuento', 'observaciones', 'contacto', 'ciudad', 'tipo_pago']
        widgets = {
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class': 'form-select'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'aplica_iva': 'Aplicar IVA (19%)',
            'descuento': 'Porcentaje de descuento',
            'observaciones': 'Observaciones adicionales',
            'contacto': 'Persona de contacto',
            'ciudad': 'Ciudad del proyecto',
            'tipo_pago': 'Método de pago',
        }

    aplica_iva = forms.BooleanField(
        label="Aplicar IVA (19%)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    
    descuento = forms.DecimalField(
        label="Porcentaje de descuento",
        required=False,
        initial=0,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'max': '100'
        }),
        help_text="Ingrese un valor entre 0 y 100%"
    )

class CotizacionItemForm(forms.ModelForm):
    class Meta:
        model = CotizacionItem
        fields = ['descripcion', 'cantidad', 'unidad_medida', 'valor_unidad']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del trabajo/material'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
            'valor_unidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'descripcion': 'Descripción',
            'cantidad': 'Cantidad',
            'unidad_medida': 'Unidad',
            'valor_unidad': 'Valor Unitario',
        }
        
# forms.py

class CotizacionRevisarForm(forms.ModelForm):
    aplica_iva = forms.BooleanField(
        required=False,
        label='Aplicar IVA (19%)',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'id_aplica_iva'
        })
    )

    class Meta:
        model = Cotizacion
        fields = ['tipo_pago', 'descuento', 'contacto', 'ciudad']
        widgets = {
            'tipo_pago': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_tipo_pago'
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'id': 'id_descuento'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_contacto'
            }),
            'ciudad': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_ciudad'
            }),
        }
        labels = {
            'descuento': 'Porcentaje de descuento'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descuento'].widget.attrs.update({'placeholder': '0-100%'})
        if self.instance:
            self.fields['aplica_iva'].initial = self.instance.aplica_iva

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.aplica_iva = self.cleaned_data.get('aplica_iva', False)
        if commit:
            instance.save()
        return instance

class CotizacionItemIngenieroForm(forms.ModelForm):
    class Meta:
        model = CotizacionItem
        fields = ['descripcion', 'cantidad', 'valor_unidad', 'unidad_medida']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_descripcion'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control item-cantidad',
                'step': '0.01',
                'min': '0.01',
                'id': 'id_cantidad'
            }),
            'valor_unidad': forms.NumberInput(attrs={
                'class': 'form-control item-valor',
                'step': '0.01',
                'min': '0',
                'required': 'required',
                'id': 'id_valor_unidad'
            }),
            'unidad_medida': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_unidad_medida'
            }),
        }

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    email = forms.EmailField(max_length=254, required=True, help_text='Requerido. Usa una dirección válida.')
    
    # Nuevos campos para el perfil
    telefono = forms.CharField(max_length=20, required=False, help_text='Opcional.')
    direccion = forms.CharField(widget=forms.Textarea, required=False, help_text='Opcional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'direccion', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit)
        telefono = self.cleaned_data.get('telefono')
        direccion = self.cleaned_data.get('direccion')

        # Crear perfil asociado
        perfil, creado = PerfilUsuario.objects.get_or_create(user=user)
        perfil.telefono = telefono
        perfil.direccion = direccion
        perfil.save()
        return user
    
from .models import PerfilUsuario

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['avatar', 'rol'] 

from django import forms
from .models import PerfilUsuario
from django.contrib.auth.models import User

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['avatar', 'telefono', 'direccion']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        
        subject = render_to_string(subject_template_name, context).strip()
        html_message = render_to_string(html_email_template_name, context)
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()
