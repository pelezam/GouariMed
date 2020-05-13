from django.urls import path
from . import views


urlpatterns =[
    path('', views.client_list, name="client_list"),
    path('<int:pk>/detail/', views.client_detail, name="client_detail"),
    path('<int:pk>/disable/', views.client_desactiver, name="client_disable"),
]