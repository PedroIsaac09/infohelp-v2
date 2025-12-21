from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import PerfilUsuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nome Completo",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:border-primary focus:ring-primary focus:ring-opacity-50 px-4 py-2'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:border-primary focus:ring-primary focus:ring-opacity-50 px-4 py-2'
        })
    )
    telefone = forms.CharField(
        label="Número de Telefone",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:border-primary focus:ring-primary focus:ring-opacity-50 px-4 py-2',
            'placeholder': '(11) 98765-4321'
        })
    )
    localizacao = forms.CharField(
        label="Localização",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:border-primary focus:ring-primary focus:ring-opacity-50 px-4 py-2',
            'placeholder': 'Cidade, Estado'
        })
    )

    class Meta:
        model = PerfilUsuario
        fields = ['telefone', 'localizacao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar first_name e email do User se disponível
        if self.instance.usuario:
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['email'].initial = self.instance.usuario.email

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Salvar first_name e email no User
        if self.instance.usuario:
            self.instance.usuario.first_name = self.cleaned_data['first_name']
            self.instance.usuario.email = self.cleaned_data['email']
            if commit:
                self.instance.usuario.save()
        if commit:
            instance.save()
        return instance


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:border-primary focus:ring-primary focus:ring-opacity-50 px-4 py-2',
            'placeholder': '••••••••'
        })
    )
    new_password1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:border-primary focus:ring-primary focus:ring-opacity-50 px-4 py-2',
            'placeholder': '••••••••'
        })
    )
    new_password2 = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:border-primary focus:ring-primary focus:ring-opacity-50 px-4 py-2',
            'placeholder': '••••••••'
        })
    )


class PerfilFotoForm(forms.ModelForm):
    foto = forms.ImageField(
        label="Foto de Perfil",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 px-4 py-2',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = PerfilUsuario
        fields = ['foto']
