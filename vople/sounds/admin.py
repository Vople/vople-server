from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(models.CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.EventLike)
class EventLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Gift)
class GiftAdmin(admin.ModelAdmin):
    pass
