from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from levelupapi.models import Event, Gamer, GameType, Game


class EventTests(APITestCase):

    def setUp(self):

        # Define the URL path for registering a Gamer
        url = '/register'

        # Define the Gamer properties
        gamer = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
    # Initiate POST request and capture the response
        response = self.client.post(url, gamer, format='json')

        # Store the TOKEN from the response data
        self.token = Token.objects.get(pk=response.data['token'])

        # Use the TOKEN to authenticate the requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        game_type = GameType()
        game_type.label = "Board game"

        # Save the GameType to the testing database
        game_type.save()
        self.game = Game.objects.create(
            game_type=game_type,
            title="Monopoly",
            maker="Hasbro",
            gamer_id=1,
            num_of_players=5,
            skill_level=2
        )


    def test_retrieve(self):
        # TODO: Test the event retrieve method
        event = Event.objects.create(
            organizer_id=1,
            game=self.game,
            time="12:30:00",
            date="2021-12-23",
            description="Game night"
        )
        url = f'/events/{event.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], event.id)
        self.assertEqual(response.data['date'], event.date)
        self.assertEqual(response.data['time'], event.time)
        self.assertEqual(response.data['description'], event.description)
        self.assertEqual(response.data['organizer']['id'], event.organizer.id)