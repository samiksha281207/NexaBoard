from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('add-project/', views.add_project, name='add_project'),
    path('tasks/', views.tasks, name='tasks'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('add-task/', views.add_task, name='add_task'),
    path('project/<int:id>/', views.project_detail, name='project_detail'),
    path('edit-project/<int:id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:id>/', views.delete_project, name='delete_project'),
    path('edit-task/<int:id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:id>/', views.delete_task, name='delete_task'),
    path('team/', views.team, name='team'),
    path('add-team-member/', views.add_team_member, name='add_team_member'),
    path('delete-team-member/<int:id>/', views.delete_team_member, name='delete_team_member'),
    path('edit-team-member/<int:id>/', views.edit_team_member, name='edit_team_member'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]