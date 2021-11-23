from django.urls import path


from .views import UserGameList
from .views import UserEventList

urlpatterns = [
    path('reports/usergames', UserGameList.as_view()),
    path('reports/eventgames', UserEventList.as_view())
]
