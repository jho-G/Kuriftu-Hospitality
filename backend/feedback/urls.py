from django.urls import path

from .views import GuestFeedbackCreateView

app_name = "feedback"

urlpatterns = [
    path("", GuestFeedbackCreateView.as_view(), name="api-feedback-create"),
]
