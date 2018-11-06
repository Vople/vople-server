from django.conf.urls import url
from . import views

app_name = "sounds"
urlpatterns = [
    url (
        regex=r'^event/$',
        view=views.ListAllBoards.as_view(),
        name='events',
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
        regex=r'^event_likes/$',
        view=views.ListAllBoardLikes.as_view(),
        name='all_event_likes',
    ),

    url (
        regex=r'^gifts/$',
        view=views.ListAllGifts.as_view(),
        name='all_gifts',
    ),

    url(
        regex=r'^(?P<board_id>[0-9]+)/board_like/',
        view=views.LikeEvent.as_view(),
        name='like_event',
    ),

    url(
        regex=r'^(?P<comment_id>[0-9]+)/comment_like/',
        view=views.LikeComment.as_view(),
        name='like_comment',
    ),
    url(
        regex=r'^(?P<board_id>[0-9]+)/comment/',
        view=views.CommentOnEvent.as_view(),
        name='comment_event',
    ),

    url(
        regex=r'^(?P<board_id>[0-9]+)/board/',
        view=views.EventDetailView.as_view(),
        name='event_detail'
    ),
]