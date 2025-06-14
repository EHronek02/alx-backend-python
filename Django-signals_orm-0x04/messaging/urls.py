from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'messaging'  # For namespace

urlpatterns = [
    # Message URLs
    path('', views.message_list, name='message_list'),
    path('post/', views.post_message, name='post_message'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('<int:pk>/edit/', views.edit_message, name='edit_message'),
    
    # History URLs
    path('<int:message_id>/history/', views.message_history, name='message_history'),
    path('delete-account/', views.delete_user_confirm, name='delete_user_confirm'),
    path('delete-account/confirm/', views.delete_user, name='delete_user'),

    path('thread/<int:message_id>/', views.conversation_thread, name='conversation_thread'),
    path('reply/<int:parent_id>/', views.create_reply, name='create_reply'),
    path('', cache_page(60)(views.message_list), name='message_list'),
    path('thread/<int:message_id>/', views.conversation_thread, name='conversation_thread'),
]
