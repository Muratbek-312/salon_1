from django.db import models
from django.urls import reverse_lazy
from pytils.translit import slugify


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, primary_key=True)
    image = models.ImageField(upload_to='category')
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''


class Service(models.Model):
    # "моделька сервиса"
    title = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='service_category')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='service')

    def __str__(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('service-details', kwargs={'pk': self.id})

    def get_image_url(self):
        if self.img:
            return self.img.url
        return ''


class ServiceImage(models.Model):
    # "картинка сервиса"
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services', null=True, blank=True)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''











