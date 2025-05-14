from django.urls import path
from .views import DataProcessorView, TransformDataView, AllProductsView

urlpatterns = [
    path('process/', DataProcessorView.as_view(), name='process_data'),
    path('transform/<str:transformation_type>/', TransformDataView.as_view(), name='transform_data'),
    path('products/', AllProductsView.as_view(), name='get_all_products'),
] 