from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CurrentUserView, RegisterView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("", include(router.urls)),
]
