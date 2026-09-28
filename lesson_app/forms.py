from django import forms

from .models import image


class ImageUploadForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = image
        fields = ("image",)