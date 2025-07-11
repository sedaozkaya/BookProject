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
    LEVEL_CHOICES = [
        ('primary', 'İlkokul'),
        ('middle', 'Ortaokul'),
        ('high', 'Lise'),
        ('university', 'Üniversite'),
        ('general', 'Genel'),
    ]

    title = models.CharField(max_length=200)  # Ürün adı için
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='general')  # Seviye için

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
    image = models.ImageField( upload_to='listing_images/',default='listing_images/default.png',blank=True,null=True)

    def __str__(self):
        return f"{self.title} - {self.get_level_display()}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"


class Interested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username} ilgileniyor: {self.listing.title}"


class Conversation(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='buyer_conversations', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='seller_conversations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation: {self.listing.title} - {self.buyer.username} & {self.seller.username}'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
