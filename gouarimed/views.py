from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from client.forms import ProfileForm, ExtendedUserCreationForm
from django.contrib.auth.decorators import login_required
from client.models import Profile
from django.contrib.auth.models import User


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
            data = {
                'last_name': form.cleaned_data['last_name'],
                'first_name': form.cleaned_data['first_name'],
                'email': request.POST.get('email'),
                'telephone': request.POST.get('telephone'),
                'pays': request.POST.get('pays'),
            }
            ctx = {'form': form, "data": data}
            return render(request, 'registration/sign_up.html', ctx)
    else:
        return render(request, 'registration/sign_up.html')


@login_required
def profil_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    if not request.user.is_superuser:
        client = get_object_or_404(Profile, user=user)
    return render(request, 'profile.html', locals())