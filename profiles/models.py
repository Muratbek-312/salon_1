from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_customer')
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=300, blank=True, default='no bio...')
    avatar = models.ImageField(upload_to='avatars/', default='default-avatar.jpg')
    phone = PhoneNumberField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        to_slug = str(self.user.nik_name)
        self.slug = to_slug
        super().save(*args, **kwargs)


class MasterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_master')
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='master_img', default='img.jpg')
    is_master = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse_lazy('master_details', kwargs={'pk': self.id})

    def has_perm(self, perm, obj=None):
        return self.is_master

    def save(self, *args, **kwargs):
        to_slug = str(self.user.nik_name)
        self.slug = to_slug
        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''


class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        ordering = ["-value"]


class Rating(models.Model):
    user = models.CharField(max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE, verbose_name='мастер', related_name='master')

    def __str__(self):
        return f"{self.star} - {self.master}"

    class Meta:
        ordering = ["-star"]


class Comment(models.Model):
    master = models.ForeignKey(MasterProfile, on_delete=models.CASCADE, related_name='master_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Оставил комментарии {self.user} на продукт {self.master}'
