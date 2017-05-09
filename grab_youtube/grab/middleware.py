import logging
from django.http.response import HttpResponse
from django.shortcuts import render
from raven.contrib.django.models import sentry_exception_handler
# from social_auth.strategy import SocialAuthCookieException

logger = logging.getLogger(__name__)

class GrabException(Exception):
    pass

class UserException(GrabException):
    pass

class ForbiddenException(GrabException):
    pass

class UnauthorizedException(GrabException):
    pass

class ExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, UnauthorizedException):
            status = 401
        elif isinstance(exception, ForbiddenException):
            status = 403
        else:
            status = 500

        # if isinstance(exception, UnauthorizedException):
        #     return render(request, 'error_unauthorized.html', {'message': exception.message}, status=status)

        if isinstance(exception, ForbiddenException):
            return render(request, 'error_forbidden.html', {'message': exception.message}, status=status)

        # if isinstance(exception, SocialAuthCookieException):
        #     return render(request, 'auth_error.html', {'error_message': exception.message}, status=status)
