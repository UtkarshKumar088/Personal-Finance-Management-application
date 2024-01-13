# urls.py
from django.contrib import admin
from django.urls import path,include
from base.views import create_expense, edit_expense, delete_expense, view_expense
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='base/login_page.html'), name='login'), 
    path('create_expense/', create_expense, name='create_expense'),
    path('edit_expense/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('view_expense/', view_expense, name='view_expense'),
    path('accounts/', include('allauth.urls')), 
]
