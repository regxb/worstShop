from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('verify/<uuid:code>', views.EmailVerificationView.as_view(), name='email_verification'),
    path('wishlist/', login_required(views.UserWishListView.as_view()), name='wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='wishlist_add'),
    path('wishlist/delete/', views.delete_from_wishlist, name='wishlist_delete'),
]
