from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('booking/new/', views.new_booking.as_view(), name='new'),
    path('booking/select/', views.booking_select.as_view(), name='select'),
    path('booking/success/', views.booking_success.as_view(), name='success'),
    path('QDyDjq/', views.AdminLogin.as_view(), name='admin_login'),
    path('QDyDjq/view/', views.AdminView.as_view(), name='admin_view'),
    # path('QDyDjq/booking/<int:pk>/', views.booking_detail.as_view(), name='booking_detail'),
]
