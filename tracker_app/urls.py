from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ideas/list/", views.idea_list, name="idea_list"),
    path("ideas/new/", views.idea_create, name="idea_create"),
    path("ideas/<int:pk>/edit/", views.idea_edit, name="idea_edit"),
    path("ideas/<int:pk>/delete/", views.idea_delete, name="idea_delete"),
    path("ideas/<int:pk>/toggle-favorite/", views.idea_toggle_favorite, name="idea_toggle_favorite"),
    path("ideas/<int:pk>/summarize/", views.idea_summarize, name="idea_summarize"),
    path("login/", views.login, name="login"),
    path("signup/", views.register, name="signup"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
]