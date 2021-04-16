from django.urls import path

from .views import CategoryView, ServiceListView, ServiceDetailsView, ServiceCreateView, ServiceEditView, ServiceDeleteView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index-page'),
    path('service/', CategoryView.as_view(), name='category'),
    path('service/create/', ServiceCreateView.as_view(), name='create-service'),
    path('service/<slug:category_slug>/', ServiceListView.as_view(), name='service-list'),
    path('service/details/<int:pk>/', ServiceDetailsView.as_view(), name='service-details'),
    path('service/edit/<int:pk>/', ServiceEditView.as_view(), name='edit-service'),
    path('service/delete/<int:pk>/', ServiceDeleteView.as_view(), name='delete-service'),
]
