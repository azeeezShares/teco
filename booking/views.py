from datetime import timezone
import json
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Branch, Client, Service, Booking, Admin


# function to check sesssion data before rendering
def check_session_data(request):
    return True if request.session.get('first_name') and request.session.get('phone') else False

# function to clear session data
def clear_session(request):
    del request.session['first_name']
    del request.session['phone']

# Home view
class HomeView(TemplateView):
    template_name = 'index.html'

# New booking view
class new_booking(TemplateView):
    template_name = 'booking/new.html'
    
    def get(self, request, *args, **kwargs):
        if request.GET.get('reset') == 'true':
            clear_session(request)
            return redirect('new')
        
        # check if the session has data
        if check_session_data(request):
            return redirect('select')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["details"] = {
            "state": "new_booking",
        }
        return context

    # save data in session
    def post(self, request, *args, **kwargs):
        data = request.POST
        # check if the data is valid
        if not data.get('first_name') or not data.get('phone'):
            # use message framework to display error
            messages.error(request, _('Please fill in all required fields.'), extra_tags='alert alert-danger')
            return redirect('new')
        # save data in session
        request.session['first_name'] = data.get('first_name', '')
        request.session['last_name'] = data.get('last_name', '')
        request.session['phone'] = data.get('phone', '')
        request.session['email'] = data.get('email', '')
        request.session['additional_details'] = data.get('additional_details', '')
        request.session['receive_special_offers'] = data.get('receive_special_offers', False)
        # redirect to the next step
        return redirect('select')
        

class booking_select(View):
    template_name = 'booking/select.html'
    
    def get(self, request, *args, **kwargs):
        if not check_session_data(request):
            return redirect('new')
        
        context = {
            "details": {
                "state": "select_service_branch",
            }
        }
        
        # get all services
        context['services'] = Service.objects.all()
        
        # get all branches
        context['branches'] = Branch.objects.all()
        
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        if not check_session_data(request):
            return redirect('new')
        
        
        data = request.POST
        # check if the data is valid
        if not data.get('service') or not data.get('branch') or not data.get('date') or not data.get('time'):
            # use message framework to display error
            messages.error(request, _('Please fill in all required fields.'), extra_tags='alert alert-danger')
            return redirect('select')
        # get the client
        client = Client.objects.create(
            first_name=request.session.get('first_name', ''),
            last_name=request.session.get('last_name', ''),
            phone_number=request.session.get('phone', ''),
            email=request.session.get('email', ''),
            additional_details=request.session.get('additional_details', ''),
            receive_special_offers=request.session.get('receive_special_offers', False)
        )
        # get the services
        services = Service.objects.filter(pk__in=data.getlist('service'))
        # get the branch
        branch = Branch.objects.get(pk=data.get('branch'))
        # save the booking
        for service in services:
            booking = Booking.objects.create(
                client=client,
                service=service,
                branch=branch, 
                booking_datetime=f"{data.get('date')} {data.get('time')}",
            )
        
        # clear session
        clear_session(request)
        
        # use message framework to display success
        messages.success(request, _('Booking has been created successfully.'), extra_tags='alert alert-success')
        # redirect to the success page
        context = {
            "details": {
                "state": "booking_success",
                "booking": booking,
            }
        }
        return render(request, 'booking/success.html', context=context)
    
class booking_success(TemplateView):
    template_name = 'booking/success.html'
    

# admin view for booking
class AdminLogin(TemplateView):
    template_name = 'booking/admin.html'
    
    def get(self, request, *args, **kwargs):
        # check if the admin is already logged in
        if request.session.get('admin'):
            return redirect('admin_view')
        return render(request, self.template_name, context={})
    
    # handle login
    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data)
        if data.get('login') and data.get('password'):
            # get admin and check if it exists
            print(request.POST)
            admin = Admin.objects.filter(username=data.get('login'), password=data.get('password')).first()
            if not admin:
                # use message framework to display error
                messages.error(request, _('Invalid credentials.'), extra_tags='alert alert-danger')
                return redirect('admin_login')
            # save the admin in session
            request.session['admin'] = admin.pk
            return redirect('admin_view')
        # use message framework to display error
        messages.error(request, _('Invalid credentials.'), extra_tags='alert alert-danger')
        return redirect('admin_login')

# admin view for booking  
class AdminView(View):
    template_name = 'booking/admin_view.html'
    
    def get(self, request, *args, **kwargs):
        # check if admin logged in
        if not request.session.get('admin'):
            return redirect('admin_login')
        context = {}
        context['items'] = Booking.objects.all()
        return render(request, self.template_name, context=context)
    
# View to handle cookie consent
class CookieConsentView(View):
    def post(self, request:HttpRequest, *args, **kwargs):
        try:
            consent = json.loads(request.body.decode('utf-8'))['consent']
        except KeyError:
            return HttpResponse("Invalid JSON", status=400)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)
        
        print(consent)
        
        # check text for consent accepted/rejected
        
        
        if consent != True:
            # User has not accepted cookies
            response =  HttpResponse("Cookie consent not accepted")
            response.set_cookie('consent', 'rejected', max_age=365*24*60*60) # 1 year
            return response
        
        # User has accepted cookies
        response = HttpResponse("Cookie consent accepted")
        response.set_cookie('consent', 'accepted', max_age=365*24*60*60) # 1 year
        return response
    def get(self, request, *args, **kwargs):
        # Check if the cookie is already set
        if request.COOKIES.get('consent') == 'accepted':
            return HttpResponse("Cookie consent already accepted")
        elif request.COOKIES.get('consent') == 'rejected':
            return HttpResponse("Cookie consent REJECTED")
        else:
            # Cookie consent not set yet
            return HttpResponse("Cookie consent not set")