from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),

    # Tabs
    path('tabs/', views.TabListCreateView.as_view(), name='tab-list-create'),
    path('tabs/<int:pk>/', views.TabDetailView.as_view(), name='tab-detail'),

    # Comments
    path('tabs/<int:tab_id>/comments/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # Favorites
    path('tabs/<int:tab_id>/favorite/', views.FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite-list'),
]