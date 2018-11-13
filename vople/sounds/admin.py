from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'title',
        'content',
        'joined_member',
        'script',
        'mode',
        'due_date',
        'comments',
        'board_likes',
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
        'comment_plots',
        'owner',
        'board',
        'content',
        'sound',
        'comment_likes',
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
        'casts',
        'id',
        'scripts',
    )

@admin.register(models.Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = (
        'script',
        'roll_name',
        'is_adjust',
        'member',
        'plots_by_cast',
        'id',
    )