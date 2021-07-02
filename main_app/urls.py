from django.contrib import admin
from django.urls import path
from .views import CheckStructure, LoginView, GetStructure

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='get_code'),
    path('structure/', GetStructure.as_view(), name='get_structure'),
    path('check_structure/', CheckStructure.as_view(), name='check_structure')
]
