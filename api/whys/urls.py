from django.urls import path
from .views import ImportView, DetailModelsView, DetailModelIdView, DeleteAllView

urlpatterns = [
    path('import/', ImportView.as_view(), name='import'),
    path('detail/<str:model_name>/', DetailModelsView.as_view(), name='detail_models'),
    path('detail/<str:model_name>/<int:id>/', DetailModelIdView.as_view(), name='detail_model_id'),
    # Add rather unsafe delete of all data for testing purposes
    path('delete-all/', DeleteAllView.as_view(), name='delete_all_models'),
]