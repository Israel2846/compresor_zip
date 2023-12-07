from django import forms
from .models import *

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombres_usuario', 'appat_usuario',
                  'apmat_usuario', 'num_empleado', 'num_tel', 'email', 'rol',]
        widgets = {
            'nombres_usuario': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'appat_usuario': forms.TextInput(attrs={'placeholder': 'Apellido paterno'}),
            'apmat_usuario': forms.TextInput(attrs={'placeholder': 'Apellido materno'}),
            'num_empleado': forms.NumberInput(attrs={'placeholder': 'Número de empleado'}),
            'num_tel': forms.NumberInput(attrs={'placeholder': 'Número de contacto'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'rol': forms.Select(attrs={'class': 'ui dropdown', 'required': 'required'}),
        }

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'id': 'password1',
            'required': 'required',
            'placeholder': 'Contraseña'
        }
    ))

    password2 = forms.CharField(label='Contraseña de confirmación', widget=forms.PasswordInput(
        attrs={
            'id': 'password1',
            'required': 'required',
            'placeholder': 'Confirmar contraseña'
        }
    ))
