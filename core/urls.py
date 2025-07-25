

from django.urls import path
from .views import register
from .views import calculator
from .views import save_operation
from .views import clear_history

urlpatterns = [
    path('register/', register, name='register'),
    path('calculadora/', calculator, name='calculadora'),
    path('save_operation/', save_operation, name='save_operation'),
    path('clear_history/', clear_history, name='clear_history'),
]
