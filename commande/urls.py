from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/', include([
        path('', views.categorie, name='categorie_list'),
        path('add', views.categorie, name='categorie_add'),
        path('<int:id>/edit/', views.categorie_edit, name='categorie_edit'),
        path('<int:id>/detail/', views.categorie_detail, name='categorie_detail'),
        path('<int:id>/delete/', views.categorie_delete, name='categorie_delete'),
        path('<int:id>/produits/', views.produit_by_categorie, name="produit_by_categorie"),
    ])),

    path('produits/', include([
        path('', views.produit_list, name="produit_list"),
        path('add', views.produit_add, name="produit_add"),
        path('<int:id>/edit/', views.produit_edit, name="produit_edit"),
        path('<int:id>/detail/', views.produit_detail, name="produit_detail"),
        path('<int:id>/delete/', views.produit_delete, name="produit_delete"),
    ])),

    path('commandes/', views.commande_list, name="commande_list"),
    path('list-commandes/', views.commande_list_admin, name="commande_list_admin"),
    path('commandes/create/', views.commande_add, name="commande_add"),
    path('commandes/<int:id>/detail', views.commande_detail, name="commande_detail"),

]
