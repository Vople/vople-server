from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'title',
        'content',
        'script',
        'mode',
        'due_date',
        'id',
    )

@admin.register(models.CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BoardLike)
class BoardLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'board',
        'content',
        'sound',
        'id',
    )

@admin.register(models.Present)
class PresentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = (
        'cast',
        'comment',
        'id',
        'order',
    )

@admin.register(models.Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'member_restriction',
        'is_accept',
        'title',
        'id',
    )

@admin.register(models.Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = (
        'roll_name',
        'id',
    )

@admin.register(models.Casting)
class CastingAdmin(admin.ModelAdmin):
    list_display = (
        'script',
        'cast',
        'is_adjust',
        'member',
    )