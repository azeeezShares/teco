from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('booking.urls')),
)

urlpatterns += [
    path('set_language/', set_language, name='set_language'),
]