from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, 
        max_length=30, 
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu Nombre"})
    )
    last_name = forms.CharField(
        required=True, 
        max_length=30, 
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu Apellido"})
    )
    email = forms.EmailField(
        required=True, 
        help_text="Requerido. Ingresa un correo válido.",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Elige una contraseña"}),
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repite tu contraseña"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]  # Usa el email como nombre de usuario
        if commit:
            user.save()
        return user
