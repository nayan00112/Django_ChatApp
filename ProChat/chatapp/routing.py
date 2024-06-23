from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/sc/<str:room_name>/", consumers.MySyncCon.as_asgi()),
    path("ws/ac/<str:room_name>/", consumers.MyASyncCon.as_asgi()),
]