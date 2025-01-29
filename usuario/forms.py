from django import forms
from core.models import Profile, Empresa

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'correo', 'dni', 'password', 'is_empresa']
        widgets = {
            'password': forms.PasswordInput(),
        }


class ProfileFormEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username','correo','dni',]


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'direccion', 'pais']
