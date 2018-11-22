from django.db import models
from vople.users.models import User
from fcm.models import AbstractDevice

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cast(TimeStampedModel):
    #script = models.ForeignKey(Script, on_delete=models.DO_NOTHING, related_name="casts")
    roll_name = models.CharField(max_length=20)

    def __str__(self):
        return self.roll_name

class Script(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    member_restriction = models.IntegerField(default=0, null=False)
    is_accept = models.BooleanField(default=False)
    title = models.CharField(max_length=100, default="__REMOVE__")
    casts = models.ManyToManyField(
        Cast,
        through='Casting',
        through_fields=('script', 'cast'),
    )

    def __str__(self):
        return self.title

class Casting(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    cast = models.ForeignKey(Cast, on_delete=models.CASCADE)
    is_adjust = models.BooleanField(default=False)
    member = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, related_name="my_castings", null=True)

    def __str__(self):
        return "[" + self.script.title + "]" + self.cast.roll_name + "역의 배역"

class Present(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Like(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

class Board(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="my_boards")
    present = models.ForeignKey(Present, on_delete=models.DO_NOTHING, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField(default="_REMOVE_")
    due_date = models.DateTimeField(null=True, blank=True)
    joined_member = models.ManyToManyField(User, blank=True)
    script = models.ForeignKey(Script, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="scripts") # scripts->boards
    mode = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING, null=True, related_name="comments")
    content = models.TextField(blank=True, null=True)
    sound = models.FileField(null=True)

    def __str__(self):
        return self.board.title


class Plot(TimeStampedModel):
    content = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, null=True, related_name="comment_plots", blank=True)
    order = models.IntegerField(default=0)
    # Add Field
    cast = models.ForeignKey(Cast, related_name="plots_by_cast", null=True, blank=True, on_delete=models.DO_NOTHING)


    def __str__(self):
        if self.cast is not None:
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

class MyDevice(AbstractDevice):
    user = models.ForeignKey(User, related_name="devices", on_delete=models.PROTECT)