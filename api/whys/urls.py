from django.urls import path
from .views import ImportView, DetailModulesView, DetailModuleIdView

urlpatterns = [
    path('import/', ImportView.as_view(), name='import'),
    path('detail/<str:module_name>/', DetailModulesView.as_view(), name='detail_modules'),
    path('detail/<str:module_name>/<int:id>/', DetailModuleIdView.as_view(), name='detail_module_id'),
]