from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm


@login_required
def image_create(request):
    if request.method == "POST":
        # Form is sent
        form = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # Form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Image added successfully")

            # redirect to new created item detail view
            return redirect('dashboard')
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, "image/create.html", {"section": "images", "form": form})

