from django import forms
from .models import Categorie, Produit, Commande


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


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ('profile', )
