from django.shortcuts import redirect, render

from .forms import ImageUploadForm
from .models import image


def home(request):
    form = ImageUploadForm()
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

    images = image.objects.order_by("-created_at")
    return render(
        request,
        "lesson_app/lesson.html",
        {"image": images, "upload_form": form},
    )