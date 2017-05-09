from grab_youtube.account.models import Profile


class AccountMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        if request.user.is_authenticated():
            try:
                profile = Profile.objects.get(user=request.user)
                request.__class__.profile = profile

            except Profile.DoesNotExist:
                request.__class__.profile = None
        else:
            request.__class__.profile = None
