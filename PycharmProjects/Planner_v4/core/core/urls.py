from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
	path('logout/', views.custom_logout, name="logout"),
	path('pdf/', views.pdf , name='pdf'),
	path('admin/', admin.site.urls),
	path('login/' , views.login_page, name='login'),
	path('register/', views.register_page, name='register'),

	path('planner/', views.planner, name='planner'),
	path('update_planner/<int:id>', views.update_planner, name='update_planner'),
	path('delete_planner/<int:id>', views.delete_planner, name='delete_planner'),
	path('show_urls/', views.show_urls, name='show_urls'),
]
