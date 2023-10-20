from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from post import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('post_to_twitter/', views.post_to_twitter, name='post_to_twitter'),
    path('login/', views.twitter_login, name='twitter_login'),
    path('callback/', views.twitter_callback, name='twitter_callback'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
