from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanel.as_view(), name="user-panel-page"),
    path('edit-info/', views.EditInfoUserPage.as_view(), name="edit-info-page"),
    path('change-password/', views.ChangePasswordPage.as_view(), name="change-password_page")
]
