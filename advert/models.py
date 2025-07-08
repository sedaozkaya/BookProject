from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    TYPE_CHOICES = [
        ('book', 'Kitap'),
        ('note', 'Ders Notu'),
    ]
    DONATION_TYPE_CHOICES = [
        ('free', 'Bağış'),
        ('paid', 'Ücretli'),
    ]
    RESOLUTION_LEVEL_CHOICES = [
        ('low', 'Az Çözülmüş'),
        ('medium', 'Orta Çözülmüş'),
        ('high', 'Çok Çözülmüş'),
        ('full', 'Hepsi Çözülmüş'),
    ]

    listing_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    donation_type = models.CharField(max_length=10, choices=DONATION_TYPE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    page_count = models.PositiveIntegerField()
    related_course = models.CharField(max_length=100)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    valid_year = models.PositiveIntegerField(blank=True, null=True)
    resolution_level = models.CharField(max_length=10, choices=RESOLUTION_LEVEL_CHOICES, blank=True, null=True)
    publish_year = models.PositiveIntegerField(blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_listing_type_display()} - {self.related_course}"
