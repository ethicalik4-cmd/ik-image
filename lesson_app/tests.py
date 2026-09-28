from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image as PillowImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import image

# Create your tests here.


class ImageUploadTests(TestCase):
	def test_home_displays_gallery_and_upload_form(self):
		response = self.client.get(reverse("home"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Add an image")
		self.assertContains(response, "No images have been added yet.")

	def test_upload_saves_valid_image(self):
		with TemporaryDirectory() as media_root:
			with override_settings(MEDIA_ROOT=media_root):
				image_data = BytesIO()
				PillowImage.new("RGB", (1, 1)).save(image_data, format="PNG")
				uploaded_file = SimpleUploadedFile(
					"sample.png", image_data.getvalue(), content_type="image/png"
				)

				response = self.client.post(
					reverse("home"), {"image": uploaded_file}
				)

				self.assertRedirects(response, reverse("home"))
				saved_image = image.objects.get()
				self.assertTrue(saved_image.image.storage.exists(saved_image.image.name))

	def test_upload_rejects_non_image_file(self):
		response = self.client.post(
			reverse("home"),
			{"image": SimpleUploadedFile("notes.txt", b"not an image")},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Upload a valid image")
		self.assertEqual(image.objects.count(), 0)
