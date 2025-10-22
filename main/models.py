from django.db import models
from django.utils.text import slugify
import uuid
import random
import string

class Rapat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.judul)
            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            self.slug = f"{base_slug}-{random_str}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.judul
    
    class Meta:
        ordering = ['-created_at']

class Menu(models.Model):
    rapat = models.ForeignKey(Rapat, on_delete=models.CASCADE, related_name='menus')
    nama = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nama} - {self.rapat.judul}"
    
    class Meta:
        ordering = ['nama']

class Pesanan(models.Model):
    rapat = models.ForeignKey(Rapat, on_delete=models.CASCADE, related_name='pesanans')
    nama_pemesan = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nama_pemesan} - {self.rapat.judul}"
    
    class Meta:
        ordering = ['created_at']

class PesananItem(models.Model):
    pesanan = models.ForeignKey(Pesanan, on_delete=models.CASCADE, related_name='items')
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)
    custom_request = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        if self.menu:
            return f"{self.menu.nama} x{self.quantity}"
        return f"{self.custom_request} x{self.quantity}"
