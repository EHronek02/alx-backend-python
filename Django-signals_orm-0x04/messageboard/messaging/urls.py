from django.urls import path
from . import views

app_name = 'messaging'  # For namespace

urlpatterns = [
    # Message URLs
    path('', views.message_list, name='message_list'),
    path('post/', views.post_message, name='post_message'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('<int:pk>/edit/', views.edit_message, name='edit_message'),
    
    # History URLs
    path('<int:message_id>/history/', views.message_history, name='message_history'),
]
