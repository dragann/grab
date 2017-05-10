import json
import urllib
import urlparse

import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, authenticate
from django.utils import timezone
from social_django.models import UserSocialAuth
from django.contrib import auth
from django.contrib.auth import login as auth_login

from grab_youtube import settings
from grab_youtube.account.forms import PasswordForm
from grab_youtube.account.models import Profile
from grab_youtube.grab.middleware import ForbiddenException
from grab_youtube.grab.utils import render_to_json
from grab_youtube.videos.models import YoutubeVideo, VideoRating


def home(request):
    return redirect(user_detail)


def logout(request):
    auth_logout(request)
    return home(request)


@login_required()
def user_detail(request, slug=None):
    exclude_privacy = []
    if not slug:
        slug = request.profile.slug

    profile = Profile.objects.get(slug=slug)
    if profile != request.profile :
        exclude_privacy = ['SELF']
        if request.profile not in profile.friends.all():
            raise ForbiddenException()

    filter = request.GET.get('filter', None)
    sort = request.GET.get('sort', YoutubeVideo._meta.ordering[0])

    videos_by_year = profile.videos.filter(archived_at__isnull=True).exclude(privacy__in=exclude_privacy).extra(select={'year': "EXTRACT(year FROM shared_at)"}).values('pk', 'year')
    filters = ['all']
    for video in videos_by_year:
        if str(video['year']) not in filters:
            filters.append(str(video['year']))

    videos = profile.videos.exclude(privacy__in=exclude_privacy)

    if videos.filter(archived_at__isnull=False).count() > 0:
        if request.profile == profile:
            filters.append('archived')
    else:
        if filter == 'archived':
            filter = 'all'

    if filter == 'archived':
        if request.profile != profile:
            back_url = _get_back_url(request)
            raise ForbiddenException({'back_url': back_url})

        videos = videos.filter(archived_at__isnull=False)
    else:
        videos = videos.filter(archived_at__isnull=True)

    if not filter:
        filter = 'all'
    if filter not in ['all', 'archived']:
        date = datetime.datetime.strptime(filter, "%Y").date()
        videos = videos.filter(shared_at__gte=date, shared_at__lt=date.replace(year = date.year + 1))

        if videos.count() == 0:
            videos = profile.videos.filter(archived_at__isnull=True)
            filter = 'all'

    videos = videos.order_by(sort)
    profile_hearts = []
    profile_poos = []
    for rating in request.profile.video_ratings.filter(video__in=videos).select_related('video').values_list('rating', 'video'):
        if rating[0] == 'heart':
            profile_hearts.append(rating[1])
        if rating[0] == 'poo':
            profile_poos.append(rating[1])

    if videos.count() == 0:
        filters = []

    icon_class = 'icon-arrow-up2'
    label = 'A - Z'
    if '-' in sort:
        icon_class = 'icon-arrow-down2'
        if 'title' in sort:
            label = 'Z - A'

    if 'shared' in sort:
        label = 'Date'

    return render(request, 'user_detail.html', locals())


def _get_data(url, data=[]):
    res = json.loads(requests.get(url).text)
    data.extend(res['data'])

    if 'paging' in res and 'next' in res['paging']:
        next = res['paging']['next']
        _get_data(next, data)

    return data


@login_required()
def sync_videos(request, slug):
    profile = Profile.objects.get(slug=slug)
    if request.profile != profile:
        raise ForbiddenException()


    social_user = UserSocialAuth.objects.get(user=profile.user)
    url = '{0}{1}/posts?fields=attachments,privacy,created_time,from&limit=500&access_token={2}'.format('https://graph.facebook.com/', social_user.uid, social_user.access_token)
    if profile.synced_at:
        since = profile.synced_at.strftime('%s')
        url = '{0}&since={1}'.format(url, since)



    # EXCEPTIONS
    # post_id = '1152747214870504_185071148304787'
    # post_id = '1152747214870504_1154988577979701'
    # post_id = '1448618438501797_987906881243177'
    # token = 'EAAOsb3noDjMBALRUBOMMVkdiHuDU1rawpuw6AghBZCYWtE95VopaNLR1IC7d5WC6lcZCPXZCDXdMhxkN7Gy0t7wnZAUZA8ZC61ZAEb9XgoTL32xfq5YyZCzNkXIydinOj3qo4VTUeUcu2xZCpTzDeWnbrtVEx6PtNZC7OX1viBXxNTZByqDnyjOIphO'
    # url = '{0}{1}?fields=attachments,privacy,created_time,from&access_token={2}'.format('https://graph.facebook.com/', post_id, token)
    # res = json.loads(requests.get(url).text)
    # special_data = [res]
    # print special_data
    # return_now = True
    # if return_now:
    #     return HttpResponse()




    data = _get_data(url)
    existing_video_ids = list(profile.videos.all().values_list('post_id', flat=True))
    new_video_count = 0

    for post in data:
        post_id = post['id']
        privacy = post['privacy']['value']
        if post_id in existing_video_ids:
            continue

        if not 'attachments' in post:
            continue

        post_data = post['attachments']['data']

        if len(post_data) == 0:
            continue
        post_data = post_data[0]

        if not post_data['type'] == 'video_share_youtube':
            continue

        video_url = urlparse.urlparse(urllib.unquote(post_data['url']))
        url_data = urlparse.parse_qs(video_url.query)

        if 'v' in url_data:
            youtube_id = url_data['v'][0]
        else:
            url_data = url_data['u']
            query = ''
            if len(url_data) == 1:
                query = url_data[0]
            else:
                for el in url_data:
                    if 'watch' in el:
                        query = el

            parsed_url_data = urlparse.urlparse(query)
            youtube_url = urlparse.parse_qs(parsed_url_data.query)

            if 'v' in youtube_url:
                youtube_id = youtube_url['v'][0]
            else:
                youtube_id = parsed_url_data.path[1:]

        thumbnail_url = 'img.youtube.com/vi/{0}/0.jpg'.format(youtube_id)

        YoutubeVideo.objects.create(
            profile=profile,
            shared_at=post['created_time'],
            title=post_data['title'],
            youtube_id=youtube_id,
            thumbnail_url=thumbnail_url,
            post_id=post_id,
            privacy=privacy,
        )

        new_video_count += 1
        existing_video_ids.append(post_id)

    profile.synced_at = timezone.now()
    profile.save()

    return HttpResponse(new_video_count)

@login_required()
def video_detail(request, video_id):
    video = YoutubeVideo.objects.get(pk=video_id)

    if request.profile != video.profile and video.privacy == 'SELF':
        raise ForbiddenException()

    back_url = _get_back_url(request)

    return render(request, 'video_detail.html', locals())


@login_required()
def get_video_thumb_url(request, video_id):
    thumb = YoutubeVideo.objects.get(pk=video_id).get_thumbnail_url()
    return HttpResponse(thumb)


@login_required()
def friends_list(request, slug):
    profile = Profile.objects.get(slug=slug)
    if profile != request.profile:
        raise ForbiddenException()

    friends = profile.friends.all()
    return render(request, 'friends_list.html', locals())


@login_required()
def delete_videos(request, slug):
    profile = Profile.objects.get(slug=slug)
    if profile != request.profile:
        raise ForbiddenException()

    profile.videos.all().delete()
    profile.synced_at = None
    profile.save()

    return redirect(user_detail, slug)


@login_required()
def archive_video(request, video_id):
    video = YoutubeVideo.objects.get(pk=video_id)

    if request.profile != video.profile:
        raise ForbiddenException()

    video.archived_at = timezone.now()
    video.save()

    return HttpResponse()


@login_required()
def restore_video(request, video_id):
    video = YoutubeVideo.objects.get(pk=video_id)

    if request.profile != video.profile:
        raise ForbiddenException()

    video.archived_at = None
    video.save()

    return HttpResponse()


@login_required()
def rate_video(request, video_id):
    video = YoutubeVideo.objects.get(pk=video_id)
    if request.profile == video.profile:
        return HttpResponse('own video', status=500)

    rating = request.GET.get('rating', '')
    if not rating:
        return HttpResponse('no rating specified', status=500)

    try:
        video_rating = VideoRating.objects.get(profile=request.profile, video=video)
        if rating == video_rating.rating:
            video_rating.delete()
        else:
            video_rating.rating = rating
            video_rating.save()

    except VideoRating.DoesNotExist:
        VideoRating.objects.get_or_create(profile=request.profile, video=video, rating=rating)

    return HttpResponse()


@login_required()
def profile_settings(request, slug):
    profile = Profile.objects.get(slug=slug)
    alert_settings = False
    user = profile.user
    if profile != request.profile:
        raise ForbiddenException()

    has_password = profile.user.has_usable_password()

    if request.method == 'POST':
        if has_password:
            password_form = PasswordChangeForm(user, request.POST)
            message = 'Your password was changed'
        else:
            password_form = SetPasswordForm(user, request.POST)
            message = 'Your password was set'

        if password_form.is_valid():
            password = password_form.cleaned_data['new_password1']
            password_form.save()
            user = authenticate(username=user.email, password=password)
            auth_login(request, user)

            return render_to_json({'success': message})

        return render_to_json({'errors': password_form.errors})

    else:
        if has_password:
            password_form = PasswordChangeForm(user)
        else:
            password_form = SetPasswordForm(user)

    return render(request, 'settings.html', locals())


@login_required()
def delete_user(request, slug):
    profile = Profile.objects.get(slug=slug)
    action = request.GET.get('action')
    if request.profile != profile:
        raise ForbiddenException()

    if action == 'delete':
        profile.user.delete()

    if action == 'disable':
        profile.user.is_active = False
        profile.user.save()
        auth_logout(request)

    return redirect(home)


def _get_back_url(request):
    back_url = None
    referer = request.META.get('HTTP_REFERER', '')
    host = request.META.get('HTTP_HOST', '')
    parsed_referer = urlparse.urlparse(referer)

    if host == parsed_referer.netloc:
        if parsed_referer.query:
            back_url = '{0}?{1}'.format(parsed_referer.path, parsed_referer.query)
        else:
            back_url = parsed_referer.path


    return back_url