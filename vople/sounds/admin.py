from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    pass

@admin.register(models.CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BoardLike)
class BoardLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Present)
class PresentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'sound',
        'cast',
    )

@admin.register(models.Script)
class ScriptAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Cast)
class CastAdmin(admin.ModelAdmin):
    pass