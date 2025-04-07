from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('booking/new/', views.new_booking.as_view(), name='new'),
    path('booking/select/', views.booking_select.as_view(), name='select'),
    path('booking/success/', views.booking_success.as_view(), name='success'),
    
    # path for cookies
    path('cookie-consent/', views.CookieConsentView.as_view(), name='cookie_consent'),
    
]