from django.contrib import admin

from .models import MasterProfile, Comment, Rating, RatingStar, CustomerProfile


admin.site.register(RatingStar)


@admin.register(Comment)
class CommentProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "body", "master", "created", "updated")


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "email")


@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "master", "user")

