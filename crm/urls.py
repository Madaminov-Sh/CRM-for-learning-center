from django.contrib import admin
from django.urls import path, include
from leads.views import HomeView, SignupView
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetCompleteView,
 PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', HomeView.as_view()),
    path('', include('leads.urls', namespace='leads')),
    path('agents/', include('agents.urls', namespace = 'agents')),
    path('signup/', SignupView.as_view(),name="signup"),
    path('login/', LoginView.as_view(),name="login"),
    path('password-reset-view/', PasswordResetView.as_view(), name = 'password_reset_view'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password-reset-complete-done/', PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name="logout")
]
