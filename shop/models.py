from django.db import models
import uuid
from io import BytesIO
from django.core.files import File
import qrcode

class Menu(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='categories')
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.menu.name} - {self.name}"


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name



class TableQRCode(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    code = models.CharField(max_length=64, unique=True)
    table_number = models.CharField(max_length=30, blank=True, null=True)
    qr_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # ساخت QR Code خودکار برای لینک منو
        qr_url = f"http://127.0.0.1:8000/m/{self.code}/"
        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        file_name = f"{self.code}.png"
        self.qr_image.save(file_name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menu.name} - {self.code}"
