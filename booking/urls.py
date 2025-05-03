from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('booking/new/', views.new_booking.as_view(), name='new'),
    path('booking/select/', views.booking_select.as_view(), name='select'),
    path('booking/success/', views.booking_success.as_view(), name='success'),
    
    # path for branches
    path('branch/<str:branch_name>/', views.BranchView.as_view(), name='branch_view'),
    
    # path for cookies
    path('cookie-consent/', views.CookieConsentView.as_view(), name='cookie_consent'),
    
    path('politica-de-cookies/', views.PoliticaDeCookies.as_view(), name='politica_de_cookies')
    
]