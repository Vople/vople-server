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

    def __str__(self):
        return self.owner

class Board(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    present = models.ForeignKey(Present, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    due_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

class Comment(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    content = models.TextField(null=True)

    def __str__(self):
        return self.content

class BoardLike(Like):
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING, null=False)

    def __str__(self):
        return self.owner
    

class CommentLike(Like):
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, null=False)

    def __str__(self):
        return self.owner