from django import forms
from core import models
from django.core.exceptions import ValidationError
from datetime import date

class profile_form_model(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = 'username', 'password', 'correo', 'dni','imagen_perfil','is_empresa','empresa_id'
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user