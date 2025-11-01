# StudyAI_Project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

# Import your custom view class
from core.views import CustomLoginView 
# StudyAI_Project/urls.py (Add this import near the top)
from django.contrib.auth.views import LogoutView # <--- CRITICAL FIX

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🚨 FIX: Call the class-based view's as_view() method
    path('accounts/login/', CustomLoginView.as_view(), name='login'), 
    
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    # Django Auth URLs (used for logout, password reset)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Root path: directs all requests to the 'core' app's URLs
    path('', include('core.urls')), 
]

if settings.DEBUG:
    # Include browser reload URLs
    urlpatterns += [
        path('__reload__/', include('django_browser_reload.urls')),
    ]
    # Serves media files during local development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)