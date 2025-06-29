
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.urls import include

from onlineshop.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('onlineshop/', include('onlineshop.urls')),
]
from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/onlineshop/', permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += [
    path('sign-up', RegisterView.as_view(), name='sign-up'),
]
from django.conf import settings
from django.conf.urls.static import static

# ... your existing urlpatterns ...

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

