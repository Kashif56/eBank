from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
import datetime

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check session timeout
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = datetime.datetime.fromisoformat(last_activity)
                if (timezone.now() - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    messages.warning(request, 'Your session has expired due to inactivity.')
                    return redirect('account_login')
            
            # Update last activity time
            request.session['last_activity'] = timezone.now().isoformat()

            # Check if user is locked out
            if hasattr(request.user, 'account'):
                if request.user.account.is_locked and request.path != '/accounts/logout/':
                    logout(request)
                    messages.error(request, 'Your account has been locked due to security concerns. Please contact support.')
                    return redirect('account_login')

        response = self.get_response(request)
        return response
