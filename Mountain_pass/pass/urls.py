from django.urls import path
from .views import PassageAPIView, reverse_to_submit


urlpatterns = [
    path('submitData/', PassageAPIView.as_view({'post': 'post', 'get': 'get_records_by_user'}), name='submitData'),
    path('submitData/<int:pk>', PassageAPIView.as_view({'patch': 'edit_one_record', 'get': 'get_one'})),
    path('', reverse_to_submit),
]
