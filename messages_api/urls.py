from django.urls import path
from .views import MessageHistoryView

urlpatterns = [
    path(
        "messages/history",
        MessageHistoryView.as_view(),
        name="message-history"
    ),
]