from django.contrib import admin

from .models import Category, Service, ServiceImage


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug', )
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')


class ServiceImagesInline(admin.TabularInline):
    model = ServiceImage
    fields = ('image', )


class ServiceAdmin(admin.ModelAdmin):
    inlines = (ServiceImagesInline, )
    list_display = ('id', 'title', 'price')
    list_display_links = ('id', 'title')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
