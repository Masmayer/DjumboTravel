from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class LoginView(View):
    """ Login view for dashboard """
    template_name = 'customauth/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            nif = request.POST.get('userid')
            password = request.POST.get('password')
            user = authenticate(nif=nif, password=password)
            if user:
                login(request, user)
                return redirect('inventory:dashboard')
            else:
                messages.error(request, "Invalid username or password!")
            print(nif, password)
        return render(request, self.template_name)


class LogoutView(View):
    """ Logout view for dashboard """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('customauth:login')
