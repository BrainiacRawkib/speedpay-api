from django.contrib import admin
from django.urls import path, include
from users.views import LoginAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/login/', LoginAPIView.as_view()),
]
