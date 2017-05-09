import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from social_django.models import UserSocialAuth
from sorl.thumbnail import get_thumbnail


class Profile(models.Model):
    user = models.ForeignKey(User)
    slug = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    friends = models.ManyToManyField('self')
    fb_user_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, null=True, blank=True)

    def get_avatar_url(self, size):
        try:
            return get_thumbnail(self.avatar_url, size, crop='center', format='JPEG', quality=100).url
        except:
            pass

    def avatar_url_large(self):
        return self.get_avatar_url('150x150')

    def avatar_url_small(self):
        return self.get_avatar_url('90x90')

    @property
    def name(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.get_full_name()) or "%d" % random.randint(10000, 99999)

            while Profile.objects.filter(slug=self.slug).exists():
                self.slug = "%s-%d" % (self.slug[:249], random.randint(10000, 99999))

        if not self.fb_user_id:
            self.fb_user_id = UserSocialAuth.objects.get(user=self.user).uid

        super(Profile, self).save(*args, **kwargs)

    def rated_videos(self):
        print self.video_ratings.all()
