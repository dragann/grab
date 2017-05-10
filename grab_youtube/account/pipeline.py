from social_django.models import UserSocialAuth
import json
import requests
from grab_youtube.account.models import Profile


def save_profile(user, **kwargs):
    if not kwargs['is_new']:
        return

    fbuid = kwargs['uid']
    access_token = kwargs['response']['access_token']
    url = '{0}{1}?fields=picture.type(large),friends,email,gender&access_token={2}'.format('https://graph.facebook.com/', fbuid, access_token)
    data = json.loads(requests.get(url).text)

    profile, created = Profile.objects.get_or_create(user=user)
    profile.avatar_url = data['picture']['data']['url']
    profile.fb_user_id = fbuid
    profile.gender = data['gender']
    profile.save()
    user.email = data['email']
    user.username = data['email']
    user.save()

    friends = Profile.objects.filter(fb_user_id__in=[friend['id'] for friend in data['friends']['data']])
    for friend in friends:
        profile.friends.add(friend)

    return {'profile': profile}
