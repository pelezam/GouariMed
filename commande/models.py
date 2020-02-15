from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class Profile(models.Model):
    telephone = models.CharField(max_length=165)
    pays = models.CharField(max_length=255)
    structure = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.last_name}"


class Categorie(models.Model):
    libelle = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.libelle


class Produit(models.Model):
    libelle = models.CharField(max_length=255, unique=True)
    prix = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.libelle


class EmailorUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
