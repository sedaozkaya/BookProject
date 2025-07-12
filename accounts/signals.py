
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='BookLoop’a Hoş Geldiniz!',
            message=f'Merhaba {instance.first_name or instance.username},\n\nBookLoop’a katıldığınız için teşekkür ederiz! İlan vererek kitap & not paylaşmaya hemen başlayabilirsiniz.',
            from_email='bookloop.destek@gmail.com',
            recipient_list=[instance.email],
            fail_silently=False,
        )
