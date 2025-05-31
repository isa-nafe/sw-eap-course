from django.urls import path
from . import views

app_name = 'course'
urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('planner/', views.course_planner_view, name='course_planner'),
    path('materials/', views.course_materials_list_view, name='course_materials_list'),
    path('materials/<int:material_id>/', views.serve_protected_material, name='serve_protected_material'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    # We will add more URLs here for registration, login, etc.
]
