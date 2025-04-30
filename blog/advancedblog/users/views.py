from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.http import HttpResponse
from .models import Profile

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':  # Bu satır fonksiyon tanımından sonra girintili olmalı
        form = UserRegisterForm(request.POST)  # 4 boşluk girinti
        if form.is_valid():  # 4 boşluk daha
            form.save()  # 8 boşluk girinti
            username = form.cleaned_data.get('username')  # 8 boşluk
            messages.success(request, f'Hesabınız oluşturuldu! Artık giriş yapabilirsiniz.')  # 8 boşluk
            return redirect('login')  # 8 boşluk
    else:  # 4 boşluk (if ile aynı hizada)
        form = UserRegisterForm()  # 8 boşluk
    return render(request, 'users/register.html', {'form': form})  # 4 boşluk (fonksiyon bloğu içinde)

@login_required
def profile(request):
    # Check if user doesn't have a profile
    if not hasattr(request.user, 'profile'):
        # Create a new profile if one doesn't exist
        Profile.objects.create(user=request.user)
    
    # Always render the profile template
    return render(request, 'users/profile.html', {
        'user': request.user,
        'profile': request.user.profile
    })
@login_required
def profile_update(request):
    # Get or create profile for the user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after update
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'users/profile_update.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

        

