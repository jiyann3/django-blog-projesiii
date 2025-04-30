from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

def user_directory_path(instance, filename):
    # upload_to path will be MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def profile_pic_path(instance, filename):
    # Profil resimleri için kayıt yolu: media/profile_pics/user_<id>/<filename>
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default='default.jpg', 
        upload_to=profile_pic_path
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Profil resmini boyutlandırma (opsiyonel)
        img = Image.open(self.profile_picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)


# Kullanıcı oluşturulduğunda otomatik profil oluştur
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()