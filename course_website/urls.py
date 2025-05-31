from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Required for media serving
from django.conf.urls.static import static # Required for media serving

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('course.urls')), # Includes all URLs from the 'course' app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
