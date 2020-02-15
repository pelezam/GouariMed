from django import forms
from .models import Profile, Categorie, Produit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProduitForm(forms.ModelForm):

    class Meta:
        model = Produit
        fields = '__all__'

    def clean_libelle(self):
        libelle = self.cleaned_data['libelle']
        libelle = libelle.lower()

        return libelle


class CategorieForm(forms.ModelForm):

    class Meta:
        model = Categorie
        fields = '__all__'

    def clean_libelle(self):
        libelle = self.cleaned_data['libelle']
        libelle = libelle.lower()
        return libelle


class ExtendedUserCreationForm(UserCreationForm):
    last_name = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']

        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('telephone', 'structure', 'pays')
