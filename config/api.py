from django.urls import path
from rest_framework import routers

from panda.apps.transactions.views import TransactionViewSet, UploadsView, ApiRoot

router = routers.SimpleRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

app_name = 'api'
urlpatterns = router.urls + [
    path('uploads/', UploadsView.as_view(), name=UploadsView.name),
    path('', ApiRoot.as_view(), name=ApiRoot.name)
]
