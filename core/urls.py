

from django.urls import path
from .views import register
from .views import calculator
from .views import save_operation
from .views import clear_history
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('register/', register, name='register'),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('calculadora/', calculator, name='calculadora'),
    path('save_operation/', save_operation, name='save_operation'),
    path('clear_history/', clear_history, name='clear_history'),
]
