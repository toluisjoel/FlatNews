import re
from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'account/profile.html', {'section': 'profile'})


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(request, user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': user_form})
