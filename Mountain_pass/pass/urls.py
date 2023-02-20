from django.urls import path
from .views import PassageAPIView


urlpatterns = [
    path('submitData/', PassageAPIView.as_view({'post': 'post', })),
]
