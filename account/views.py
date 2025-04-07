from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from booking.models import Branch, Client, Service, Booking, Admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _

class AdminLogin(TemplateView):
    template_name = 'booking/admin.html'
    
    def get(self, request:HttpRequest, *args, **kwargs):
        print(request.user.is_authenticated)
        # check if the admin is already logged in
        if request.user.is_authenticated:
            return redirect('admin_view')
        return render(request, self.template_name, context={})
    
    def post(self, request, *args, **kwargs):
        # check if the admin is already logged in
        if request.user.is_authenticated:
            return redirect('admin_view')
        # check if the data is valid
        if not request.POST.get('login') or not request.POST.get('password'):
            # use message framework to display error
            messages.error(request, _('Please fill in all required fields.'), extra_tags='alert alert-danger')
            return redirect('admin_login')
        
        user = authenticate(request, email=request.POST.get('login'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('admin_view')
        else:
            # use message framework to display error
            messages.error(request, _('Invalid credentials.'), extra_tags='alert alert-danger')
            return redirect('admin_login')
        
class AdminView(View):
    template_name = 'admin-temp/view.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        context['items'] = Booking.objects.all()
        return render(request, self.template_name, context=context)