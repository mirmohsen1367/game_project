
from app.views.user_view import UserView
from app.views.store_view import StoreView
from rest_framework import routers

app_urls = routers.DefaultRouter()

app_urls.register(r"user", viewset=UserView, basename="user")
app_urls.register(r"store", viewset=StoreView, basename="store")
