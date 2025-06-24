from django import forms
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm:

    def clean_url(self):
        url = self.clean_data["url"]
        valid_extensions = ["jpq", "jpeq"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not match valid image extensions."
            )
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.clean_data["url"]
        image_name = "{}.{}".format(
            slugify(image.title), image_url.rsplit(".", 1)[1].lower()
        )
        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image
