from django.contrib.auth.decorators import login_required, user_passes_test
from commande.models import Commande
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.contrib.auth.models import User

@user_passes_test(lambda u: u.is_superuser)
def client_list(request):
    clients = Profile.objects.all()
    return render(request, 'client/client_list.html', {"clients": clients})


@user_passes_test(lambda u: u.is_superuser)
def client_detail(request, pk):
    try:
        client = Profile.objects.get(pk=pk)
        commandes = Commande.objects.filter(profile=client).order_by('-date')
    except Profile.DoesNotExist:
        pass
    else:
        return render(request, 'client/client_detail.html', {'client': client, 'commandes': commandes})


@user_passes_test(lambda u: u.is_superuser)
def client_desactiver(request, pk):
    client = get_object_or_404(Profile, pk=pk)
    user = get_object_or_404(User, profile=client)
    user.is_active = False if user.is_active else True
    user.save()
    return redirect('client_detail', pk=pk)