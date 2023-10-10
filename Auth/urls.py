from django.urls import path
from . import views

app_name = 'Auth'


urlpatterns = [
    path('users/', views.CreateListUser.as_view()),
    path('users/update/<user_id>/', views.UpdateUser.as_view()),
    path('users/me/<user_id>/', views.RetrieveUser.as_view()),
    path('users/delete/<user_id>/', views.DeleteUser.as_view()),
    path('users/createsuperuser/', views.CreateSuperUser.as_view()),
    path('users/forgot-password/', views.ForgotPassword.as_view()),
    path('users/reset-password/', views.ResetPassword.as_view()),
    path('users/activate/<user_id>/', views.ActivateUser.as_view()),

]

