from .models import Profile
from django.shortcuts import render
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def profile(request):
    return render(request, 'account/profile.html', {'section': 'profile'})


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_edit_form = UserEditForm(instance=request.user, data=request.POST)
        profile_edit_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit_form.save()
            profile_edit_form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        messages.success(request, 'Error updating your profile')
        user_edit_form = UserEditForm(instance=request.user)
        profile_edit_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_edit_form, 'profile_form': profile_edit_form})
