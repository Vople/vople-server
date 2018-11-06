from django.db import models
from vople.users.models import User

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Present(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=50, null=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Like(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

class Board(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    present = models.ForeignKey(Present, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=100, null=False, default="_REMOVE_")
    content = models.TextField(null=False, default="_REMOVE_")
    due_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

class Comment(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING, null=True, related_name="comments")
    content = models.TextField(null=True)
    sound = models.FileField(null=True)

    def __str__(self):
        return self.board.title

class BoardLike(Like):
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING, null=False, related_name="board_likes")

    def __str__(self):
        return self.owner.username + " : " + self.board.title
    

class CommentLike(Like):
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, null=False, related_name="comment_likes")
