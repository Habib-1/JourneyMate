from django.urls import path
from .import views
urlpatterns = [
   path('register/',views.register.as_view(),name='register'),
   path('login/',views.login,name='login'),
   path('logout/',views.logout,name='logout'),
   path('profile/',views.profile,name='profile'),
   path('edit_profile/',views.edit_profile,name='edit_profile'),

]