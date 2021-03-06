from django.conf.urls import url
from . import views
from rest_framework import routers

app_name = "sounds"


urlpatterns = [
    url (
        regex=r'^board/$',
        view=views.ListAllBoards.as_view(),
        name='boards',
    ),

    url(
        regex=r'^(?P<board_id>[0-9]+)/join/$',
        view=views.JoinBoardViewSet.as_view(),
        name='join_board',
    ),

    url (
        regex=r'^comments/$',
        view=views.ListAllComments.as_view(),
        name='all_comments',
    ),
    url (
        regex=r'^(?P<board_id>[0-9]+)/comments/$',
        view=views.ListCommentsOnBoard.as_view(),
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
        regex=r'^(?P<board_id>[0-9]+)/board_like/',
        view=views.LikeBoard.as_view(),
        name='like_board',
    ),

    url(
        regex=r'^(?P<comment_id>[0-9]+)/comment_like/',
        view=views.LikeComment.as_view(),
        name='like_comment',
    ),
    url(
        regex=r'^(?P<board_id>[0-9]+)/comment/',
        view=views.CommentOnBoard.as_view(),
        name='comment_board',
    ),

    url(
        regex=r'^(?P<board_id>[0-9]+)/board/',
        view=views.BoardDetailView.as_view(),
        name='board_detail',
    ),
    url(
        regex=r'^scripts/$',
        view=views.ScriptViewSet.as_view(),
        name='script',
    ),
    url(
        regex=r'^(?P<script_id>[0-9]+)/script/',
        view=views.GetScriptView.as_view(),
        name='get_script',
    ),
    url(
        regex=r'^(?P<board_id>[0-9]+)/plots/',
        view=views.GetPlotView.as_view(),
        name='get_plots',
    ),
    url(
        regex=r'^event/',
        view=views.GetEventBoardView.as_view(),
        name='event_board',
    ),
]