from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('telephone', 'structure', 'pays')

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        telephone = telephone.replace('_', '')
        return telephone


class ExtendedUserCreationForm(UserCreationForm):
    last_name = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.filter(email=email)
            if u:
                raise forms.ValidationError('Cet email est déjà utilisé')
        except User.DoesNotExist:
            pass

        return email


