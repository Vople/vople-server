from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class ListAllEvents(APIView):
    def get(self, request, format=None):

        events = models.Event.objects.all()

        paginator = Paginator(events, 20)

        page = request.query_params.get('page')

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
        
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)


        serializer = serializers.EventSerializer(events, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

        #queryset = models.Event.objects.all()
        #serializer_class = serializers.EventSerializer

        #filter_backends = (filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
        #search_fields = ('job_name', 'company')
        #filter_fields = ('job_name', 'company')
        #ordering_fields = ('job_name','company')
        #ordering = ('job_name')

        #pagination_class = serializers.PaginatedEventSerializer


        #return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        user = request.user

        serializer = serializers.InputEventSerializer(data=request.data)

        gift_id = request.data['gift_id']

        try:
            found_gift = models.Gift.objects.get(id=gift_id)
        except models.Gift.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save(
                owner = user,
                gift = found_gift,
                )

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListAllComments(APIView):
    def get(self, request, format=None):

        all_comments = models.Comment.objects.all()

        serializer = serializers.CommentSerializer(all_comments, many=True)

        return Response(data=serializer.data)

class ListAllEventLikes(APIView):
    def get(self, request, format=None):

        all_event_likes = models.EventLike.objects.all()

        serializer = serializers.EventLikeSerializer(all_event_likes, many=True)

        return Response(data=serializer.data)

class ListAllCommentLikes(APIView):
    def get(self, request, format=None):

        all_comment_likes = models.CommentLike.objects.all()

        serializer = serializers.CommentLikeSerializer(all_comment_likes, many=True)

        return Response(data=serializer.data)

class ListAllGifts(APIView):
    def get(self, request, format=None):

        all_gifts = models.Gift.objects.all()

        serializer = serializers.GiftSerializer(all_gifts, many=True)

        return Response(data=serializer.data)

class LikeEvent(APIView):
    def post(self, request, Event_id, format=None):

        user = request.user

        try:
            found_Event = models.Event.objects.get(id=Event_id)
        except models.Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preExtistingLike = models.EventLike.objects.get(
                owner=user,
                Event=found_Event
            )
            preExtistingLike.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.EventLike.DoesNotExist:

            new_like = models.EventLike.objects.create(
                owner=user,
                Event=found_Event
            )

            new_like.save()

            return Response(status=status.HTTP_201_CREATED)


class LikeComment(APIView):
    def post(self, request, comment_id, format=None):

        user = request.user

        try:
            found_comment = models.Comment.objects.get(id=comment_id)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preExtistingLike = models.CommentLike.objects.get(
                owner=user,
                comment=found_comment
            )
            preExtistingLike.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.CommentLike.DoesNotExist:

            new_like = models.CommentLike.objects.create(
                owner=user,
                comment=found_comment
            )

            new_like.save()

            return Response(status=status.HTTP_201_CREATED)

class CommentOnEvent(APIView):
    def post(self, request, Event_id, format=None):

        user = request.user

        try:
            found_event = models.Event.objects.get(id=Event_id)
        except models.Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.InputSoundSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(
                owner = user,
                Event = found_event
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    def get(self, request, Event_id, format=None):

        user = request.user

        try:
            found_event = models.Event.objects.get(id=Event_id)
        except models.Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.EventSerializer(found_event)

        return Response(data=serializer.data, status=status.HTTP_200_OK)