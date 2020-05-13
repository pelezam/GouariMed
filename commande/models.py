from django.db import models
from django.contrib.auth.models import User
from client.models import Profile


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
    dosage = models.CharField(max_length=100, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.libelle


class Commande(models.Model):
    STATUS_CHOICES = (
        ('En cours', 'En cours'),
        ('Terminer', 'Terminer'),
        ('Annuler', 'Annuler')
    )
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    date_livraison = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=65, choices=STATUS_CHOICES, default='En cours')

    def __str__(self):
        return self.profile.user.last_name


class LigneCommande(models.Model):
    qte = models.PositiveIntegerField()
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    prix_total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return "{} {} commandé par {}".format(self.qte, self.produit, self.commande.profile.user.last_name)


