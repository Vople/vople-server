from django.db import models
from vople.users.models import User

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Script(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    member_restriction = models.IntegerField(default=0, null=False)
    is_accept = models.BooleanField(default=False)
    title = models.CharField(max_length=100, null=True, default="__REMOVE__")

    def __str__(self):
        return self.title

class Cast(TimeStampedModel):
    script = models.ForeignKey(Script, on_delete=models.DO_NOTHING, null=False)
    roll_name = models.CharField(max_length=20, null=False)
    is_adjust = models.BooleanField(default=False)
    member = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, related_name="my_casts")

    def __str__(self):
        return "[" + self.script.title + "] " + self.roll_name

class Present(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=50, null=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Like(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

class Board(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="my_boards")
    present = models.ForeignKey(Present, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False, default="_REMOVE_")
    due_date = models.DateTimeField(null=True)
    joined_member = models.ManyToManyField(User, blank=True)
    script = models.ForeignKey(Script, on_delete=models.DO_NOTHING, null=True, related_name="scripts")
    mode = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING, null=True, related_name="comments")
    content = models.TextField(null=True)
    sound = models.FileField(null=True)

    def __str__(self):
        return self.board.title


class Plot(TimeStampedModel):
    content = models.TextField(null=False)
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, null=True, related_name="comment_plots", blank=True)
    order = models.IntegerField(null=False, default=0)
    # Add Field
    cast = models.ForeignKey(Cast, related_name="plots_by_cast", null=True, blank=True, on_delete=models.DO_NOTHING)


    def __str__(self):
        if self.cast is not none:
            return self.cast.roll_name + " : " + self.content
        else:
            return self.content


class BoardLike(Like):
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING, null=False, related_name="board_likes")

    def __str__(self):
        return self.owner.username + " : " + self.board.title
    

class CommentLike(Like):
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, null=False, related_name="comment_likes")

    def __str__(self):
        return self.owner.username + ": " + self.comment.board.title
