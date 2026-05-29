from django.urls import path
from . import views

app_name = 'TestBack'

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('create/', views.test_create, name='test_create'),
    path('<int:pk>/', views.test_detail, name='test_detail'),
    path('<int:pk>/update/', views.test_update, name='test_update'),
    path('<int:pk>/delete/', views.test_delete, name='test_delete'),
    path('<int:pk>/like/', views.test_like, name='test_like'),
    path('<int:pk>/scrap/', views.test_scrap, name='test_scrap'),
]