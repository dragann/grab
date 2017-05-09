def alert_badges(request):
    alert_settings = False
    if request.profile and not request.user.has_usable_password():
        alert_settings = True

    return {'alert_settings': alert_settings}