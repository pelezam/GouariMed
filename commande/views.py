from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Categorie, Produit
from .forms import CategorieForm, ProduitForm


@login_required
def categorie(request):
    categories = Categorie.objects.all()
    form = CategorieForm(request.POST)

    if request.is_ajax():
        data = {"categories": list(categories.values('id', 'libelle'))}
        return JsonResponse(data)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
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
    categorie.delete()
    return redirect('categorie_list')


@user_passes_test(lambda u: u.is_superuser)
def categorie_edit(request, id):
    categories = get_list_or_404(Categorie)
    categorie = get_object_or_404(Categorie, pk=id)
    form = CategorieForm(request.POST, instance=categorie)
    if form.is_valid():
        form.save()
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
        return render(request, 'index.html')
    else:
        return HttpResponse('log in')


@login_required
def produit_list(request):
    produits = Produit.objects.all()
    if request.is_ajax():
        pass
    elif request.method == "GET":
        ctx = {'produits': produits}
        return render(request, 'commande/produit_list.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def produit_add(request):
    form = ProduitForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect('produit_list')
    else:
        return HttpResponse(form.errors.as_json())


@user_passes_test(lambda u: u.is_superuser)
def produit_edit(request, id):
    produit = get_object_or_404(Produit, pk=id)
    form = ProduitForm(request.POST, instance=produit)

    if form.is_valid():
        form.save()
        return redirect('produit_list')
    else:
        return HttpResponse(form.errors.as_json())


@user_passes_test(lambda u: u.is_superuser)
def produit_delete(request, id):
    produit = Produit.objects.get(pk=id)
    produit.delete()
    return redirect('produit_list')


@login_required
def produit_detail(request, id):
    produit = get_object_or_404(Produit, pk=id)
    if request.is_ajax():
        data = {
            'id': produit.id,
            'libelle': produit.libelle,
            'prix': produit.prix,
            'categorie': produit.categorie.libelle,
            'description': produit.description
        }

        return JsonResponse(data)