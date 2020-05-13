from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ProtectedError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Categorie, Produit, Commande, LigneCommande
from client.models import Profile
from .forms import CategorieForm, ProduitForm
import json
from django.contrib import messages
from datetime import date


@login_required
def categorie(request):
    categories = Categorie.objects.all()
    form = CategorieForm(request.POST)

    if request.is_ajax():
        data = {"categories": list(categories.values('id', 'libelle', 'description'))}
        return JsonResponse(data)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Enregistrement effectuer avec succès")
            return redirect('categorie_list')
        else:
            ctx = {'form': form, 'categories': categories}
            return render(request, 'commande/categorie_list.html', ctx)
    elif request.method == 'GET':
        ctx = {'categories': categories}
        return render(request, 'commande/categorie_list.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def categorie_delete(request, id):
    categorie = get_object_or_404(Categorie, pk=id)
    try:
        categorie.delete()
    except ProtectedError:
        messages.error(request, 'Vous ne pouvez pas supprimer cette catégorie')
    else:
        messages.success(request, 'Suppression effectuer avec succès')
    return redirect('categorie_list')


@user_passes_test(lambda u: u.is_superuser)
def categorie_edit(request, id):
    categories = get_list_or_404(Categorie)
    categorie = get_object_or_404(Categorie, pk=id)
    form = CategorieForm(request.POST, instance=categorie)
    if form.is_valid():
        form.save()
        messages.success(request, 'La modification a été effectuer avec succès')
        return redirect('categorie_list')
    else:
        ctx = {'form': form, 'categories': categories}
        return render(request, 'commande/categorie_list.html', ctx)


@login_required
def categorie_detail(request, id):
    categorie = get_object_or_404(Categorie, pk=id)

    if request.is_ajax():
        data = {
            'id': categorie.id,
            'libelle': categorie.libelle,
            'description': categorie.description
        }
        return JsonResponse(data)
    elif request.method == 'GET':
        pass


@login_required
def dashboard(request):
    if request.user.is_superuser:
        nombre_clients = Profile.objects.all().count()
        qte_produits = Produit.objects.all().count()
        nombre_commandes = Commande.objects.all().count()
        return render(request, 'index.html', locals())
    else:
        return redirect('commande_list')


@login_required
def produit_list(request):
    produits = Produit.objects.all()
    if request.is_ajax():
        data = {"produits": list(produits.values('id', 'libelle', 'prix', 'dosage'))}
        return JsonResponse(data)
    elif request.method == "GET":
        ctx = {'produits': produits}

        return render(request, 'commande/produit_list.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def produit_add(request):
    form = ProduitForm(request.POST)
    produits = Produit.objects.all()

    if form.is_valid():
        form.save()
        messages.success(request, 'Enregistrement effectuer avec succès')
        return redirect('produit_list')
    else:
        ctx = {"form": form, "produits": produits}
        return render(request, 'commande/produit_list.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def produit_edit(request, id):
    produit = get_object_or_404(Produit, pk=id)
    produits = Produit.objects.all()
    form = ProduitForm(request.POST, instance=produit)

    if form.is_valid():
        form.save()
        messages.success(request, 'Modification effectuer avec succès', extra_tags="success")
        return redirect('produit_list')
    else:
        ctx = {"form": form, "produits": produits}
        return render(request, 'commande/produit_list.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def produit_delete(request, id):
    produit = Produit.objects.get(pk=id)
    try:
        produit.delete()
    except ProtectedError:
        messages.error(request, 'Vous ne pouvez pas supprimer ce produit car il est relié a des commandes')
    else:
        messages.success(request, 'Suppression effectuer avec succès')
    return redirect('produit_list')


@login_required
def produit_detail(request, id):
    produit = get_object_or_404(Produit, pk=id)
    if request.is_ajax():
        data = {
            'id': produit.id,
            'libelle': produit.libelle,
            'prix': produit.prix,
            'dosage': produit.dosage,
            'categorie': produit.categorie.libelle,
            'description': produit.description
        }

        return JsonResponse(data)


@login_required
def commande_list(request):
    profile = Profile.objects.get(user=request.user)
    commandes = Commande.objects.filter(profile=profile).order_by('-date')
    return render(request, 'commande/commande_list.html', {'commandes': commandes})


@user_passes_test(lambda u: u.is_superuser)
def commande_list_admin(request):
    commandes = Commande.objects.all()
    return render(request, 'commande/commande_list_admin.html', locals())


@login_required
def commande_add(request):
    if request.is_ajax():
        list_commandes = json.loads(request.POST.get('commandes'))
        date_de_livraison = request.POST.get('date_livraison')
        date_de_livraison = date_de_livraison.split('-')
        cmd = Commande()
        somme_total = 0

        try:
            profile = Profile.objects.get(user=request.user)
            cmd.profile = profile
            cmd.save()

            for item in list_commandes.values():
                ligne_cmd = LigneCommande(
                    produit=Produit.objects.get(pk=int(item['produit_id'])),
                    qte=item['qte'],
                    prix_total=item['prix_total'],
                    commande=cmd
                )
                somme_total += float(item['prix_total'])
                ligne_cmd.save()

            cmd.total = somme_total
            cmd.date_livraison = date(int(date_de_livraison[0]), int(date_de_livraison[1]), int(date_de_livraison[2]))
            cmd.save()
        except Exception as e:
            cmd.delete()
            return JsonResponse({'response': 'bad', "Exception": str(e)}, status=500)

        return JsonResponse({'response': 'ok'})

    else:
        categories = Categorie.objects.all()
        return render(request, 'commande/commande_add.html', locals())


@login_required
def commande_detail(request, id):
    if request.user.is_superuser:
        commande = Commande.objects.get(pk=id)
    else:
        try:
            profile = Profile.objects.get(user=request.user)
            commande = Commande.objects.get(pk=id, profile=profile)
        except Commande.DoesNotExist:
            return HttpResponse("Erreur lors de la requête")
    ligne_commandes = LigneCommande.objects.filter(commande=commande)
    return render(request, 'commande/commande_detail.html', locals())


@login_required
def produit_by_categorie(request, id):
    categorie = Categorie.objects.get(pk=id)
    produits = Produit.objects.filter(categorie=categorie)
    if request.is_ajax():
        data = {"produits": list(produits.values('id', 'libelle', 'prix', 'description', 'dosage'))}

        return JsonResponse(data)
