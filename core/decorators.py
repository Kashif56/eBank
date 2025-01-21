from functools import wraps
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from captcha.fields import CaptchaField
from django import forms

def require_captcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        class CaptchaForm(forms.Form):
            captcha = CaptchaField()

        if request.method == 'POST':
            form = CaptchaForm(request.POST)
            if not form.is_valid():
                return render(request, 'core/captcha.html', {'form': CaptchaForm()})
            return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view

def secure_sensitive_operation(view_func):
    """
    Decorator that combines rate limiting and CAPTCHA for sensitive operations
    """
    @ratelimit(key='user_or_ip', rate='5/m', method=['POST'])
    @require_captcha
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view
