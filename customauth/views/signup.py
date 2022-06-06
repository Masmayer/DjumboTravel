import logging
from django.views.generic import View
from django.shortcuts import render, redirect

from customauth.models import User

logger = logging.getLogger('__name__')


class SignupView(View):
    template_name = 'customauth/signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            userid = request.POST.get('userid')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                try:
                    User.objects.create_user(userid=userid, password=password)
                    return redirect('customauth:login')
                except Exception as e:
                    logger.error(f'Error creating user: {e}')
            else:
                logger.error('Password and confirm password does not match')
        return render(request, self.template_name)
