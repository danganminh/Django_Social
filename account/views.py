from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)

from .models import Profile
from images.models import Image  # make sure this import exists


@login_required
def dashboard(request):
    images = request.user.images_created.all()  # from related_name
    return render(
        request, "account/dashboard.html", {"section": "dashboard", "images": images}
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password1"])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})

    else:
        user_form = UserRegistrationForm()

    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    # Make sure the profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Sent a messages success
            messages.success(request, "Profile details updated.")
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
