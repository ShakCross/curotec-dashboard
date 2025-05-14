from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', include('apps.data_processor.interfaces.urls')),
] 