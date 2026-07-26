from django.urls import path
from . import views
from . views import login_view
from .api_views import CategoryAPIView
from.api_views import RegisterAPIView
from.api_views import LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('', views.menu, name='menu'),
    path('add-menu/', views.add_menu, name='add_menu'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/<int:id>/', views.edit_menu, name='edit_menu'),
    path('delete/<int:id>/', views.delete_menu, name='delete_menu'),
    path('signup/', views.signup, name='signup'),
    path('api/categories/', CategoryAPIView.as_view(), name='category-api' ),
    path("api/categories/<int:id>/", CategoryAPIView.as_view()),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='login-api'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]