
from rest_framework import routers
app_urls = routers.DefaultRouter()
from app.views.user_view import UserView

app_urls.register(r"user", viewset=UserView, basename="user")
