from django.urls import path  
from perfil import views

app_name = "profile"
urlpatterns = [  
    path('config/', views.ConfigView.as_view(), name="config"),

    path('edit-profile', views.ProfileEditView.as_view(), name="edit-profile"),

    path('<slug:username>', views.ProfileView.as_view(), name="user-profile"),

    path('perfil/<int:pk>/like', views.ProfileAddLike.as_view(), name='like-profile'),

    path('<int:pk>/photo/', views.EditPhotoProfile.as_view(), name='photo-profile'),
    
    path('usuarios/', views.UserListView.as_view(), name='users-profile'),

    path('usernew/', views.UserCreateView.as_view(), name='usernew'),
]