from django.conf.urls import url
from . import views

app_name = "sounds"
urlpatterns = [
    url (
        regex=r'^all/$',
        view=views.ListAllBoards.as_view(),
        name='all_boards',
    ),

    url (
        regex=r'^comments/$',
        view=views.ListAllComments.as_view(),
        name='all_comments',
    ),

    url (
        regex=r'^comment_likes/$',
        view=views.ListAllCommentLikes.as_view(),
        name='all_comment_likes',
    ),

    url (
        regex=r'^board_likes/$',
        view=views.ListAllBoardLikes.as_view(),
        name='all_board_likes',
    ),

    url (
        regex=r'^presents/$',
        view=views.ListAllPresents.as_view(),
        name='all_presents',
    ),

    url(
        regex=r'^(?P<board_id>\w+)/board_like/',
        view=views.LikeBoard.as_view(),
        name='like_board',
    ),

    url(
        regex=r'^(?P<comment_id>\w+)/comment_like/',
        view=views.LikeComment.as_view(),
        name='like_comment',
    ),

    
]