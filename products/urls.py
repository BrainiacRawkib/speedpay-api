from django.urls import path
from .views import CategoryAPIView, ProductAPIView

urlpatterns = [
    path('', ProductAPIView.as_view()),
    path('categories/', CategoryAPIView.as_view()),
]
