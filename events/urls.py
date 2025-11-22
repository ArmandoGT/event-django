from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.EventoListView.as_view(), name='list_eventos'),
    path('sharepost/<int:pk>/', views.FormEventoView.as_view(), name="sharepost"),
    path('logout/', views.LogoutUserView.as_view(), name="logoutuser"),
    path('comment/<int:pk>/', views.comment_views.as_view(), name="comment"),
    path('cadastrouser/', views.CadUserView.as_view(), name="cadastrouser"),
    path('login/', views.LoginUserView.as_view(), name="loginuser"),
    path('<slug:slug>/', views.EventoDetailView.as_view(), name='detail_event')

]

