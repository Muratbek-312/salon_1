from django.urls import path

from .views import MasterProfileListView, MasterProfileDetailView, AddStarRating, MasterProfileEditView, AddComment


urlpatterns = [
    path('master/', MasterProfileListView.as_view(), name='master_list'),
    path('master/details/<int:pk>/', MasterProfileDetailView.as_view(), name='master_details'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    path('master/edit/<int:pk>/', MasterProfileEditView.as_view(), name='edit-master'),
    path("comment/<int:pk>/", AddComment.as_view(), name="add_comment"),
]
