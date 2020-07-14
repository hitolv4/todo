from django.contrib import admin
from django.urls import path
from .views import (
    signup_user,
    current_todo,
    completed_todo,
    logout_user,
    login_user,
    create_todo,
    detail_todo,
    complete_todo,
    delete_todo,
    home
)
app_name = 'todo'
urlpatterns = [
    # Auth
    path('signup', signup_user, name='signup'),
    path('logout', logout_user, name='logout'),
    path('login', login_user, name='login'),
    # todo
    path('current_todo', current_todo, name='current_todo'),
    path('completed_todo', completed_todo, name='completed_todo'),
    path('create', create_todo, name='create_todo'),
    path('detail/<int:todo_pk>/', detail_todo, name='detail_todo'),
    path('detail/<int:todo_pk>/complete', complete_todo, name='complete_todo'),
    path('detail/<int:todo_pk>/delete', delete_todo, name='delete_todo'),
    path('', home, name='home_todo')
]
