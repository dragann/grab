from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from sorl.thumbnail import get_thumbnail

from grab_youtube.account.models import Profile
from grab_youtube.settings import PROJECT_ROOT, STATIC_ROOT, STATIC_URL


class YoutubeVideo(models.Model):
    profile = models.ForeignKey(Profile, related_name='videos')
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    shared_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    post_id = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=50, null=True, blank=True)
    position = models.PositiveIntegerField(default=0)
    thumbnail_url = models.CharField(max_length=255, null=True, blank=True)
    privacy = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-shared_at',]

    def embed_url(self):
        return 'https://www.youtube.com/embed/{0}'.format(self.youtube_id)

    def watch_url(self):
        return 'https://www.youtube.com/watch?v={0}'.format(self.youtube_id)

    def get_thumbnail_url(self):
        try:
            thumb = get_thumbnail('https://{0}'.format(self.thumbnail_url), '300x165', crop='center', format='JPEG', quality=100).url
            import os.path
            if os.path.isfile(PROJECT_ROOT + thumb):
                return thumb

            return None

        except:
            pass

    def privacy_icon(self):
        if self.privacy == 'SELF':
            return 'lock2'
        elif self.privacy == 'EVERYONE':
            return 'contrast'
        else:
            return 'users'


    @models.permalink
    def get_absolute_url(self):
        return ('grab_youtube.grab.views.video_detail', [self.id])

    def get_rating(self):
        heart = self.ratings.filter(rating='heart').count()
        poo = self.ratings.filter(rating='poo').count()

        return (heart, poo)

    @property
    def visibility(self):
        if self.privacy == 'SELF':
            return 0
        elif self.privacy == 'EVERYONE':
            return 2
        else:
            return 1


class VideoRating(models.Model):
    profile = models.ForeignKey(Profile, related_name='video_ratings')
    video = models.ForeignKey(YoutubeVideo, related_name='ratings')
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.CharField(max_length=50, null=True, blank=True, choices=(('heart', 'Fucking A!'), ('poo', "It's crap")))