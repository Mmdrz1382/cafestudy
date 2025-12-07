from django.urls import path
from .views import MenuByCode
from django.views.generic import TemplateView

urlpatterns = [
    path('api/menu/<str:code>/', MenuByCode.as_view(), name='menu-by-code'),
    path('m/<str:code>/', TemplateView.as_view(template_name='shop/menu.html'), name='menu-view'),
]
