from django.urls import path
from .views import PassageAPIView, reverse_to_submit


urlpatterns = [
    path('submitData/', PassageAPIView.as_view({'post': 'post', }), name='submitData'),
    path('', reverse_to_submit),
]
