"""grab_youtube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from grab_youtube import settings

urlpatterns = [
    url(r'^profile/(?P<slug>[-\w]+)/?$', 'grab_youtube.grab.views.user_detail', name='user_detail'),
    url(r'^profile/?$', 'grab_youtube.grab.views.user_detail', name='user_detail'),
    url(r'^/?$', 'grab_youtube.grab.views.home', name='home'),
    url(r'^profile/(?P<slug>[-\w]+)/sync-videos/?$', 'grab_youtube.grab.views.sync_videos', name='sync_videos'),
    url(r'^profile/(?P<slug>[-\w]+)/delete-videos/?$', 'grab_youtube.grab.views.delete_videos', name='delete_videos'),
    url(r'^profile/(?P<slug>[-\w]+)/settings/?$', 'grab_youtube.grab.views.profile_settings', name='profile_settings'),
    url(r'^profile/(?P<slug>[-\w]+)/friends-list/?$', 'grab_youtube.grab.views.friends_list', name='friends_list'),
    url(r'^profile/(?P<slug>[-\w]+)/delete/?$', 'grab_youtube.grab.views.delete_user', name='delete_user'),
    url(r'^get-video-thumb/(?P<video_id>\d+)/?$', 'grab_youtube.grab.views.get_video_thumb_url'),
    url(r'^video/(?P<video_id>\d+)/?$', 'grab_youtube.grab.views.video_detail'),
    url(r'^video/(?P<video_id>\d+)/archive-video/?$', 'grab_youtube.grab.views.archive_video'),
    url(r'^video/(?P<video_id>\d+)/restore-video/?$', 'grab_youtube.grab.views.restore_video'),
    url(r'^video/(?P<video_id>\d+)/rate-video/?$', 'grab_youtube.grab.views.rate_video'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)