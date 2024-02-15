from django.urls import path, include
from .import views
from rest_framework.authtoken import views as auth_view
app_name = 'api'
urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('auth/', views.UserActivationAPIView.as_view(),),
    path('create_newsletter/', views.NewsletterAPIView.as_view(), name='send'),
    path('subscribe/', views.SubscribeNewsletterAPIView.as_view(), name='subscrieb'),
    path('unsubscribe/', views.UnsubscribeNewsletterAPIView.as_view(), name='unsubscrieb'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path("api-token-auth/", auth_view.obtain_auth_token)
]
