from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.i18n import set_language
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('account.urls'), name='account'),
    path('', include('booking.urls'), name='booking'),
    path('', include('blog.urls'), name='blog'),
)

urlpatterns += [
    path('set_language/', set_language, name='set_language'),
]

urlpatterns += [
    path('froala_editor/', include('froala_editor.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)