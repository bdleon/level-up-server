from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Event, Game, Gamer
from django.contrib.auth.models import User


class EventView(ViewSet):

    def create(self, request):
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['gameId'])

        try:
            event = Event.objects.create(
                game=game,
                organizer=organizer,
                description=request.data['description'],
                date=request.data['date'],
                time=request.data['time']

            )
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(
            events, context={'request': request}, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:

            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def update(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event.date = request.data['date']
        event.time = request.data['time']
        event.description = request.data['description']
        event.game = Game.objects.get(pk=request.data['gameId'])
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class GamerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Gamer
        fields = ('user',)
        depth = 1


class EventSerializer(serializers.ModelSerializer):
    organizer = GamerSerializer()

    class Meta:
        model = Event
        fields = ('id', 'organizer', 'game', 'date', 'time', 'description')
