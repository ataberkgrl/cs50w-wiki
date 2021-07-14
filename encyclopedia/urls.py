from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage/", views.new_page, name="newpage"),
    path("edit/<str:article>/", views.edit_page),
    path("wiki/<str:article>/", views.article),
    path("random/", views.random_page),
    path("search/", views.search)
]
