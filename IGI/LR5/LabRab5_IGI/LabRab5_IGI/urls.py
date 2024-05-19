
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

# Добавьте URL соотношения, чтобы перенаправить запросы с корневого URL, на URL приложения
from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/onlineshop/', permanent=True)),
]

# Используйте static() чтобы добавить соотношения для статических файлов
# Только на период разработки
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Add Django site authentication urls (for login, logout, password management)
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

