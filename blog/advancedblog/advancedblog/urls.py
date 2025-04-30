from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from users.views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    # Özel şifre sıfırlama URL'leri (admin'den önce gelmeli)
    path('password-reset/', 
         CustomPasswordResetView.as_view(), 
         name='password_reset'),
    path('password-reset/done/', 
         CustomPasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         CustomPasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
    
    # Admin URL'i (şifre sıfırlama URL'lerinden sonra gelmeli)
    path('admin/', admin.site.urls),
    
    # Diğer URL'ler
    path('', include('blog.urls')),
    path('users/', include('users.urls')),
]

# Geliştirme ortamında medya dosyaları için
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
