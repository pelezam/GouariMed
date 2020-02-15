from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from commande.forms import ProfileForm, ExtendedUserCreationForm


def sign_up(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            email = request.POST.get('email')
            password = request.POST.get('password2')

            user = authenticate(username=email, password=password)
            
            if user:
                login(request, user)
            return redirect('dashboard')
        else:
            ctx = {'form': form}
            return render(request, 'registration/sign_up.html', ctx)
    else:
        return render(request, 'registration/sign_up.html')
